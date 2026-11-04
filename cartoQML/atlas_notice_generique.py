"""Notice CSV commune aux cartes QGIS, indépendante du traitement métier."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from qgis.core import (Qgis, QgsProcessingAlgorithm, QgsProcessingException,
    QgsProcessingParameterVectorLayer, QgsProcessingParameterString,
    QgsProcessingParameterField, QgsProcessingParameterFileDestination,
    QgsProcessingParameterFile, QgsVariantUtils, QgsWkbTypes)


class AtlasNoticeGenerique(QgsProcessingAlgorithm):
    def name(self): return 'atlas_notice_generique'
    def displayName(self): return 'Atlas — Générer une notice CSV commune'
    def group(self): return 'Atlas Culture DEPS'
    def groupId(self): return 'atlas_culture_deps'
    def createInstance(self): return AtlasNoticeGenerique()
    def shortHelpString(self):
        return ('À placer à la fin de chaque modèle. Lit la couche finale et son style QGIS, '
                'sans modifier la couche. Même structure CSV : rubrique ; parametre ; valeur. '
                'Sources : une URL par ligne. Traitements et justification sont déclaratifs. '
                'Pour des empreintes exactes, fournir facultativement un manifeste JSON : '
                '[{"role":"donnees","url":"https://…","fichier":"C:/…/source.csv"}]. '
                'Le fichier local doit être la copie réellement utilisée. Aucun téléchargement ni publication.')
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('COUCHE','Couche finale de la carte'))
        self.addParameter(QgsProcessingParameterField('CHAMP','Champ représenté (si applicable)',parentLayerParameterName='COUCHE',optional=True))
        for name,label,default,multi in [
            ('ID_CARTE','Identifiant de la carte','',''),
            ('TITRE','Titre de la carte','',''),
            ('UNITE','Unité ou nature des catégories','',''),
            ('MAILLE','Maille ou type de localisation','',''),
            ('MILLESIME_DONNEES','Millésime des données','',''),
            ('MILLESIME_GEOMETRIES','Millésime des géométries','',''),
            ('SOURCES','Sources : une URL par ligne','',True),
            ('TRAITEMENTS','Traitements réalisés : filtres, jointures, agrégations…','',True),
            ('JUSTIFICATION','Justification des choix de représentation','',True),
            ('LIMITES','Limites et précautions métier','',True),
            ('CONTROLES_AMONT','Résultats des contrôles effectués en amont','',True),
        ]:
            self.addParameter(QgsProcessingParameterString(name,label,defaultValue=default,multiLine=bool(multi),optional=name!='TITRE'))
        self.addParameter(QgsProcessingParameterFile('MANIFESTE','Manifeste des fichiers réellement utilisés (JSON, facultatif)',extension='json',optional=True))
        self.addParameter(QgsProcessingParameterFileDestination('NOTICE','Notice CSV','CSV (*.csv)'))

    def processAlgorithm(self,parameters,context,feedback):
        layer=self.parameterAsVectorLayer(parameters,'COUCHE',context)
        if not layer or not layer.isValid(): raise QgsProcessingException('Couche invalide.')
        text=lambda key:self.parameterAsString(parameters,key,context).strip()
        dest=Path(self.parameterAsFileOutput(parameters,'NOTICE',context))
        if dest.exists(): raise QgsProcessingException('La notice existe déjà : choisir un autre nom.')
        if not dest.parent.is_dir(): raise QgsProcessingException('Le dossier de sortie doit exister.')
        rows=[]
        def add(r,p,v):
            rows.append([r,p,str(v) if v is not None and str(v)!='' else 'Non renseigné'])
        add('Notice','version_schema','1.0')
        add('Notice','date_generation_utc',datetime.now(timezone.utc).isoformat())
        for key,label in [('ID_CARTE','identifiant'),('TITRE','titre'),('CHAMP','champ'),('UNITE','unite'),('MAILLE','maille')]:add('Carte',label,text(key))
        add('Dates','millesime_donnees',text('MILLESIME_DONNEES'))
        add('Dates','millesime_geometries',text('MILLESIME_GEOMETRIES'))
        sources=[u.strip() for u in text('SOURCES').splitlines() if u.strip()]
        add('Sources','nombre_urls_declarees',len(sources))
        for i,url in enumerate(sources,1):add('Sources',f'source_{i}_url',url)
        manifest=text('MANIFESTE')
        entries=[]
        if manifest:
            try:
                entries=json.loads(Path(manifest).read_text(encoding='utf-8-sig'))
                if not isinstance(entries,list):raise ValueError('Liste attendue')
                for i,e in enumerate(entries,1):
                    if not isinstance(e,dict) or not e.get('fichier'):raise ValueError('Chaque entrée doit définir fichier')
                    path=Path(e['fichier'])
                    if not path.is_absolute():path=Path(manifest).parent/path
                    digest=hashlib.sha256()
                    with path.open('rb') as f:
                        for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
                    add('Sources',f'fichier_{i}_role',e.get('role'))
                    add('Sources',f'fichier_{i}_url',e.get('url'))
                    add('Sources',f'fichier_{i}_chemin',path)
                    add('Sources',f'fichier_{i}_sha256',digest.hexdigest())
            except (OSError,ValueError,TypeError) as e:raise QgsProcessingException('Manifeste invalide : '+str(e))
        add('Sources','empreintes','Calculées sur les fichiers du manifeste déclaré' if entries else 'Non calculées : copies sources non fournies')
        add('Traitements','description_declaree',text('TRAITEMENTS'))
        add('Traitements','controles_amont_declares',text('CONTROLES_AMONT'))
        add('Representation','justification_declaree',text('JUSTIFICATION'))
        add('Representation','limites_declarees',text('LIMITES'))
        renderer=layer.renderer()
        typ=renderer.type() if renderer else 'Aucun'
        add('Representation','type_rendu_qgis',typ)
        add('Representation','extraction_style','Détaillée' if typ in ('RuleRenderer','graduatedSymbol','categorizedSymbol','singleSymbol') else 'Rendu non pris en charge en détail ; conserver le QML')
        add('Representation','avertissement','Couleurs principales résumées ; conserver le QML pour contours, tailles, expressions et symboles complexes.')
        def symbol(prefix,s):
            add('Representation',prefix+'_couleur_principale',s.color().name() if s else None)
            add('Representation',prefix+'_symbole',s.dump() if s else None)
        if typ=='RuleRenderer':
            def walk(parent,prefix='regle'):
                for i,r in enumerate(parent.children(),1):
                    k=f'{prefix}_{i}'
                    add('Representation',k+'_libelle',r.label())
                    add('Representation',k+'_expression',r.filterExpression())
                    add('Representation',k+'_sinon',r.isElse())
                    add('Representation',k+'_active',r.active())
                    symbol(k,r.symbol());walk(r,k)
            walk(renderer.rootRule())
        elif typ=='graduatedSymbol':
            add('Representation','champ_ou_expression',renderer.classAttribute())
            add('Representation','methode_qgis',renderer.classificationMethod().name())
            for i,r in enumerate(renderer.ranges(),1):
                k=f'classe_{i}'
                add('Representation',k+'_libelle',r.label());add('Representation',k+'_borne_inferieure',r.lowerValue());add('Representation',k+'_borne_superieure',r.upperValue());symbol(k,r.symbol())
            add('Representation','precision_bornes','Bornes du moteur QGIS ; consulter le QML pour leur interprétation exacte.')
        elif typ=='categorizedSymbol':
            add('Representation','champ_ou_expression',renderer.classAttribute())
            for i,r in enumerate(renderer.categories(),1):
                k=f'categorie_{i}';add('Representation',k+'_libelle',r.label());add('Representation',k+'_valeur',r.value());symbol(k,r.symbol())
        elif typ=='singleSymbol':symbol('unique',renderer.symbol())
        field=text('CHAMP');missing=0;count=0
        if field and field not in layer.fields().names():raise QgsProcessingException('Champ représenté absent de la couche.')
        for f in layer.getFeatures():
            if feedback.isCanceled():raise QgsProcessingException('Annulé.')
            count+=1
            if field and (QgsVariantUtils.isNull(f[field]) or (isinstance(f[field],str) and not f[field].strip())):missing+=1
        add('Controles','nombre_entites_finales',count)
        add('Controles','valeurs_absentes_champ',missing if field else 'Non applicable : champ non renseigné')
        add('Controles','portee','Contrôles de la couche finale seulement ; doublons sources et jointures non vérifiés par cet outil.')
        add('Couche','nom',layer.name());add('Couche','geometrie',QgsWkbTypes.displayString(layer.wkbType()));add('Couche','scr',layer.crs().authid())
        add('Environnement','qgis',Qgis.QGIS_VERSION)
        add('Sorties','notice_csv',dest)
        add('Sorties','publication','Aucune')
        with dest.open('x',encoding='utf-8-sig',newline='') as f:
            writer=csv.writer(f,delimiter=';');writer.writerow(['rubrique','parametre','valeur'])
            writer.writerows([["'"+v if v.lstrip().startswith(('=','+','-','@')) else v for v in row] for row in rows])
        return {'NOTICE':str(dest)}

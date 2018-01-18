#-*- coding:utf-8 -*-
#
# Copyright © 2016–2017 Liang Feng <finalion@gmail.com>
#
# Support: Report an issue at https://github.com/finalion/WordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from anki.lang import currentLang
trans = {
    'CHECK_FILENAME_LABEL': {'zh_CN': u'使用文件名作为标签', 'en': u'Use filename as dict label', 'fr': r"Utiliser le nom de fichier en tant qu'étiquette de dico"},
    'EXPORT_MEDIA': {'zh_CN': u'导出媒体文件', 'en': u'Export media files', 'fr': u'Exporter les fichiers multimédias'},
    'DICTS_FOLDERS': {'zh_CN': u'字典文件夹', 'en': u'Dict folders', 'fr': u'Dossiers dico'},
    'CHOOSE_NOTE_TYPES': {'zh_CN': u'选择笔记类型', 'en': u'Choose note types', 'fr': u'Choisir le type de note '},
    'CURRENT_NOTE_TYPE': {'zh_CN': u'当前类型', 'en': u'Current type', 'fr': u'Type utilisé en cours'},
    'MDX_SERVER': {'zh_CN': u'MDX服务器', 'en': u'MDX server', 'fr': u'serveur MDX'},
    'USE_DICTIONARY': {'zh_CN': u'使用字典', 'en': u'Use dict', 'fr': u'Utilisé un dico'},
    'UPDATED': {'zh_CN': u'更新', 'en': u'Updated', 'fr': u'Mettre à jour'},
    'CARDS': {'zh_CN': u'卡片', 'en': u'Cards', 'fr': u'Cartes'},
    'QUERIED': {'zh_CN': u'查询', 'en': u'Queried', 'fr': u'Quêté'},
    'FIELDS': {'zh_CN': u'字段', 'en': u'Fields', 'fr': u'Champs'},
    'WORDS': {'zh_CN': u'单词', 'en': u'Words', 'fr': u'Mots'},
    'NOT_DICT_FIELD': {'zh_CN': u'不是字典字段', 'en': u'Not dict field', 'fr': u'Pas un champ de dico'},
    'NOTE_TYPE_FIELDS': {'zh_CN': u'<b>笔记字段</b>', 'en': u'<b>Note fields</b>', 'fr': u'<b>Champ de note</b>'},
    'DICTS': {'zh_CN': u'<b>字典</b>', 'en': u'<b>Dict</b>', 'fr': u'<b>Dico</b>'},
    'DICT_FIELDS': {'zh_CN': u'<b>字典字段</b>', 'en': u'<b>Dict fields</b>', 'fr': u'<b>Champ de dico</b>'},
    'RADIOS_DESC': {'zh_CN': u'<b>单选框选中为待查询单词字段</b>', 'en': u'<b>Word field needs to be selected.</b>', 'fr': u'<b>Champ de mot doit d\'être sélectionné. </b>'},
    'NO_QUERY_WORD': {'zh_CN': u'查询字段无单词', 'en': u'No word is found in the query field', 'fr': u'Aucun est trouvé dans le champ'},
    'CSS_NOT_FOUND': {'zh_CN': u'没有找到CSS文件，请手动选择', 'en': u'No valid css stylesheets found, please choose the file', 'fr': u'Aucun fichier de style CSS est valide, veuillez choisir le fichier'},
    'ABOUT': {'zh_CN': u'关于', 'en': u'About', 'fr': u'À propos'},
    'REPOSITORY': {'zh_CN': u'项目地址', 'en': u'Project homepage', 'fr': u'Accueil du projet'},
    'FEEDBACK': {'zh_CN': u'反馈', 'en': u'Feedback', 'fr': u'Retourner de l\'information'},
    'VERSION': {'zh_CN': u'版本', 'en': u'Version', 'fr': u'Version'},
    'LATEST_VERSION': {'zh_CN': u'无更新版本.', 'en': u'No update version.', 'fr': u'Pas de mise à jour.'},
    'ABNORMAL_VERSION': {'zh_CN': u'当前版本异常.', 'en': u'The current version is abnormal.', 'fr': u'La version actuelle est anormale.'},
    'CHECK_FAILURE': {'zh_CN': u'版本检查失败.', 'en': u'Version check failure.', 'fr': u'Erreur de vérifier la version.'},
    'NEW_VERSION': {'zh_CN': u'检查到新版本:', 'en': u'New version:', 'fr': u'Nouvelle version:'},
    'UPDATE': {'zh_CN': u'更新', 'en': u'Update', 'fr': u'Mise à jour'}
}


def _(key, lang=currentLang):
    if lang != 'zh_CN' and lang != 'en' and lang != 'fr':
        lang = 'en'  # fallback

    def disp(s):
        return s.lower().capitalize()

    if key not in trans or lang not in trans[key]:
        return disp(key)
    return trans[key][lang]


def _sl(key):
    return trans[key].values()

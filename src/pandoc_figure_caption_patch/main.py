#!/bin/env python
import re
import locale
import panflute as pan
from pandoc_figure_caption_patch.lib import Log, get_siblings
SET_CITE = re.compile(r'^: ?(.*?)(\{#(.+) *\})?$')
_LANG = locale.getdefaultlocale()[0]
LANG = _LANG if _LANG else 'en_US'
I18N = {
    'warn_no_template': {
        'en_US': '⚠️ Not found `template: {temp}` as reference-doc in input metadata, you may have to adjust the format of new section, which fallback to pandoc default docx!',
        'zh_CN': '⚠️ 在元数据中未找到`template: {temp}`字段，您可能要调整新节的页边距等格式，回退到pandoc原生docx模板！',
    }
}


def get_metadata(doc: pan.Doc, key: str, default: str | None = None):
    return pan.stringify(doc.metadata[key]) if key in doc.metadata else default


def get_inner_images(elem: pan.Element):
    if not hasattr(elem, 'content'):
        return None
    imgs = [ele for ele in elem.content if isinstance(ele, pan.Image)]
    return imgs if imgs else None


def action(elem: pan.Element, doc: pan.Doc) -> pan.Para | pan.Figure | pan.Element | pan.Space | pan.Str | pan.MetaValue:
    # if not isinstance(elem, (pan.Space, pan.Str, pan.MetaValue)):
    #     Log(type(elem), str(elem)[:128])
    if IS_DOC_XML:
        if isinstance(elem, pan.Para):
            imgs_elems = get_inner_images(elem)
            if not imgs_elems:
                cite = get_cite(elem)
                cite = any(cite) if cite else None
                return pan.Para(pan.Str('')) if cite else elem
            siblings, idx = get_siblings(elem)
            # _prev_elem = siblings[idx - 1] if idx > 0 else None
            _next_elem = siblings[idx + 1] if idx < len(siblings) - 1 else None
            # _prev_cite = get_cite(_prev_elem) if _prev_elem else None
            _next_cite = get_cite(_next_elem) if _next_elem else None
            if _next_cite:
                title, _, Id = _next_cite
            else:
                return elem
            img = imgs_elems[0]  # TODO
            # Log(f'{prev_elem}⬅️{cite.groups()}➡️{next_elem}')
            _kwargs = {}
            if title:
                img.title = title
                caption = pan.Caption(pan.Plain(pan.Str(title)))
                _kwargs.update({'caption': caption})
            if Id:
                _kwargs.update({'identifier': Id})
            figure = pan.Figure(pan.Para(img), **_kwargs)
            Log(f'{figure=}')
            return figure
    # TODO: difference
    # mine:   Figure(Plain(Image(Str(I) Space Str(love); url='...')); identifier='fig:img')
    # pandoc: Figure(Para(Image(; url='...', title='uml ', identifier='fig:uml')); identifier='fig:uml')
    return elem


def get_cite(elem: pan.Element) -> tuple[str | None, str | None, str | None] | None:
    if isinstance(elem, pan.Para):
        cite = SET_CITE.search(pan.stringify(elem).strip())
        return cite.groups() if cite else None  # type: ignore
    else:
        return None


def prepare(doc: pan.Doc):
    global IS_DOC_XML
    if 'doc' in doc.format:
        IS_DOC_XML = True
    elif doc.format == 'html' or 'markdown' in doc.format:
        ...
    else:
        pan.debug(f'Skip un-implemented doc format: {getattr(doc, 'format', 'None')}')


def main(doc: pan.Doc | None = None):
    return pan.run_filters(prepare=prepare, actions=[action], doc=doc)


if __name__ == '__main__':
    main()

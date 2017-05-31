from lxml import etree

import pysplivarot



def main() :

    svg = etree.parse('abc.svg')

    svgds = {e.get('id',''):e.get('d','') for e in xpath(svg, '//svg:path')}
    A,B,C = [pysplivarot.parse_svgd(svgds[i]) for i in ['A','B','C']]

    ops = [
        'A', 'B', 'C',
        'A+B', 'B-C', 'A*C',
        'A+B-C',
        '(A+B+C)-(A*B*C)',
    ]

    text_elem = xpath1(svg, '//svg:text')

    path_new = etree.Element('path')
    xpath1(svg, '//svg:g').append(path_new)
    path_new.attrib['style'] = 'fill:lightgrey;stroke:black;stroke-width:4px;fill-opacity:0.66;'
    path_new.attrib['id'] = "result"

    for path in xpath(svg, '//svg:path') :
        path.attrib['style'] = 'fill:none;stroke:grey;stroke-width:2px;'



    for i,op in enumerate(ops) :
        res = eval(op)
        svgd = pysplivarot.format_svgd(res)
        if svgd :
            text_elem.text = op
            path_new.attrib['d'] = svgd
            svg.write('generated/abc-%d.svg'%(i+1))



def xpath(e, q) :
    return e.xpath(q, namespaces={
        'svg': 'http://www.w3.org/2000/svg',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
    })

def xpath1(e, q) :
    xs = xpath(e,q)
    return xs[0] if xs else None


if __name__ == '__main__' :
    main()

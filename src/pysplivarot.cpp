
#include <string>
#include <boost/python.hpp>


#include <2geom/pathvector.h>
#include <2geom/svg-path-parser.h>
#include <2geom/svg-path-writer.h>

#include "splivarot.h"


using namespace boost::python;

/* subclass Geom::PathVector so we can provide a python object
   without conflicting with real lib2geom bindings */
class SvgPath : public Geom::PathVector{
public:
    SvgPath(){}
    SvgPath(const Geom::PathVector& pv){
        for(unsigned i=0; i<pv.size(); ++i)
            push_back(pv[i]);
    }
};

/* path object from SVG string
   just need to convert from proper PathVector to SvgPath subclass */
SvgPath parse_svgd(const char* svgd) {
    return SvgPath(Geom::parse_svg_path(svgd));
}
std::string format_svgd(const SvgPath& p, int prec, bool optimize, bool shorthands) {
    return Geom::write_svg_path(p, prec, optimize, shorthands);
}



Geom::PathVector boolop_union(const Geom::PathVector& a, const Geom::PathVector& b){
    return sp_pathvector_boolop(a,b, bool_op_union, fill_oddEven, fill_oddEven);
}

Geom::PathVector boolop_difference(const Geom::PathVector& a, const Geom::PathVector& b){
    return sp_pathvector_boolop(b,a, bool_op_diff, fill_oddEven, fill_oddEven);
}

Geom::PathVector boolop_intersection(const Geom::PathVector& a, const Geom::PathVector& b){
    return sp_pathvector_boolop(a,b, bool_op_inters, fill_oddEven,fill_oddEven);
}




SvgPath _boolop_union(const SvgPath& a, const SvgPath& b){
    return SvgPath(boolop_union((Geom::PathVector)a,(Geom::PathVector)b));
}

SvgPath _boolop_difference(const SvgPath& a, const SvgPath& b){
    return SvgPath(boolop_difference((Geom::PathVector)a,(Geom::PathVector)b));
}

SvgPath _boolop_intersection(const SvgPath& a, const SvgPath& b){
    return SvgPath(boolop_intersection((Geom::PathVector)a,(Geom::PathVector)b));
}



BOOST_PYTHON_MODULE(_pysplivarot)
{
    /* mapping for the path type */
    class_<SvgPath>("SvgPath")
        .def("__add__", &_boolop_union)
        .def("__sub__", &_boolop_difference)
        .def("__mul__", &_boolop_intersection)
    ;

    /* path IO from/to svg string */
    def("parse_svgd", parse_svgd);
    def("format_svgd", format_svgd,
        (arg("self"), arg("prec")=-1, args("optimize")=false, arg("shorthands")=true));

    /* boolean operations on PathVectors */
    def("boolop_union", &boolop_union);
    def("boolop_difference", &boolop_difference);
    def("boolop_intersection", &boolop_intersection);

}

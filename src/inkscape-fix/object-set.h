/* object-set.h is included from livarot/Shape.h
 * but the original contains way too much crap
 */


#ifndef INKSCAPE_PROTOTYPE_OBJECTSET_H
#define INKSCAPE_PROTOTYPE_OBJECTSET_H

// boolean operation
enum bool_op
{
  bool_op_union,		// A OR B
  bool_op_inters,		// A AND B
  bool_op_diff,			// A \ B
  bool_op_symdiff,  // A XOR B
  bool_op_cut,      // coupure (pleines)
  bool_op_slice     // coupure (contour)
};
typedef enum bool_op BooleanOp;


#endif

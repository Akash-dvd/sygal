"""
Example: How to use relDt (Relationship Dictionary)

relDt is a dictionary-like class designed to store relationships between
geometric algebra expressions (GExpr objects). It was previously used in the
project but has been removed from the main codebase. This example shows how
it could be used if you wanted to implement custom relationship tracking.

Note: This is just an example - relDt is no longer used in the Sygal project.
"""

from Sygal.relDt.relDt import relDt
from Sygal.initial import *
from sympy import S

def example_basic_usage():
    """Basic usage of relDt"""
    print("=" * 60)
    print("Example 1: Basic relDt Usage")
    print("=" * 60)
    
    # Create an empty relDt
    rl = relDt()
    print(f"Empty relDt: {rl}")
    
    # Create a relDt from a dictionary
    rl2 = relDt({a1: S(1), a2: S(-1)})
    print(f"relDt from dict: {rl2}")
    
    # Update with relationships
    rl.update({a1: S(2)})
    print(f"After update: {rl}")
    
    # Access relationships
    print(f"Relationship for a1: {rl[a1]}")
    print(f"Relationship for a2: {rl.get(a2, 'Not found')}")
    
    print()


def example_box_handling():
    """Example showing how relDt handles Box objects"""
    print("=" * 60)
    print("Example 2: relDt with Box objects")
    print("=" * 60)
    
    # relDt automatically converts Box objects to their underlying mv (multivector)
    box_a1 = Box(a1.mv, S(1))
    
    rl = relDt()
    # When storing, if you pass a Box with coeff=1, it extracts the mv
    # rl.update({box_a1: S(3)})  # Would extract box_a1.mv
    
    print(f"relDt after Box handling: {rl}")
    print()


def example_relationship_tracking():
    """Example of tracking geometric relationships"""
    print("=" * 60)
    print("Example 3: Tracking Geometric Relationships")
    print("=" * 60)
    
    # Create a relDt to track inner product relationships
    inner_product_rels = relDt()
    
    # Track relationships between vectors
    # inner_product_rels.update({a1: {b1: a1|b1, b2: a1|b2}})
    
    # Copy relationships
    # copied_rels = inner_product_rels.copy()
    
    print("This demonstrates how relDt could be used for")
    print("tracking relationships between GA expressions.")
    print()


def example_nested_relationships():
    """Example of nested relationship dictionaries"""
    print("=" * 60)
    print("Example 4: Nested Relationship Structures")
    print("=" * 60)
    
    # relDt can store nested dictionaries for complex relationships
    nested = relDt()
    
    # Create a nested structure
    # nested.update({
    #     a1: relDt({b1: S(1), b2: S(-1)}),
    #     a2: relDt({b1: S(0), b2: S(2)})
    # })
    
    # Access nested relationships
    # print(f"a1 -> b1 relationship: {nested[a1][b1]}")
    
    print("relDt supports nested dictionaries for complex relationship tracking.")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("relDt Usage Examples")
    print("=" * 60 + "\n")
    
    try:
        example_basic_usage()
        example_box_handling()
        example_relationship_tracking()
        example_nested_relationships()
        
        print("=" * 60)
        print("Note: relDt has been removed from the main Sygal codebase.")
        print("These examples show how it could be used if you needed")
        print("to implement custom relationship tracking.")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure Sygal is properly initialized.")


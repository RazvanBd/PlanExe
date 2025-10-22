#!/usr/bin/env python3
"""
Verify that the pydantic dependency fix is correct.
This script checks that our pydantic constraint satisfies all known requirements.

Usage:
    python verify_dependency_fix.py
"""

def parse_version(version_str):
    """Parse a version string into a tuple of integers."""
    parts = version_str.split('.')
    return tuple(int(p) for p in parts)

def check_version_satisfies(version, constraint):
    """
    Check if a version satisfies a constraint.
    
    Simplified version checker that handles common cases:
    - >=X.Y.Z
    - <X.Y.Z
    - >=X.Y.Z,<A.B.C (combined constraints)
    """
    version_tuple = parse_version(version)
    
    # Handle combined constraints (e.g., ">=2.11.5,<3.0.0")
    if ',' in constraint:
        parts = [p.strip() for p in constraint.split(',')]
        return all(check_version_satisfies(version, part) for part in parts)
    
    # Handle >= constraint
    if constraint.startswith('>='):
        min_version = constraint[2:].strip()
        min_tuple = parse_version(min_version)
        return version_tuple >= min_tuple
    
    # Handle < constraint
    if constraint.startswith('<'):
        max_version = constraint[1:].strip()
        max_tuple = parse_version(max_version)
        return version_tuple < max_tuple
    
    return True

def main():
    print("=" * 70)
    print("Pydantic Dependency Fix Verification")
    print("=" * 70)
    
    # Define the requirements from the error message
    requirements = {
        "llama-index-workflows": ">=2.11.5",
        "llama-index-core": ">=2.8.0",
        "fastapi": ">=1.7.4,<3.0.0",
        "gradio": ">=2.0",
        "banks": "any",  # No specific constraint
    }
    
    # Our new constraint
    our_constraint = ">=2.11.5,<3.0.0"
    
    print(f"\nOur pydantic constraint: {our_constraint}")
    print("\nDependency requirements:")
    for pkg, req in requirements.items():
        print(f"  • {pkg}: pydantic {req}")
    
    # Test versions that should work
    test_versions = [
        "2.11.5",  # Minimum version
        "2.11.6",  # Patch update
        "2.12.0",  # Minor update
        "2.15.0",  # Future minor version
        "2.20.0",  # Hypothetical future version
    ]
    
    # Test versions that should NOT work
    invalid_versions = [
        "2.10.4",  # Too old (original version)
        "2.11.4",  # Just below minimum
        "3.0.0",   # Too new
    ]
    
    print("\n" + "=" * 70)
    print("Testing Valid Versions")
    print("=" * 70)
    
    all_valid_passed = True
    for version in test_versions:
        print(f"\nTesting pydantic {version}:")
        all_satisfied = True
        
        # First check our constraint
        if not check_version_satisfies(version, our_constraint):
            print(f"  ✗ Does not satisfy our constraint: {our_constraint}")
            all_satisfied = False
            all_valid_passed = False
            continue
        
        # Then check all dependency requirements
        for pkg, req in requirements.items():
            if req == "any":
                satisfied = True
            else:
                satisfied = check_version_satisfies(version, req)
            
            status = "✓" if satisfied else "✗"
            print(f"  {status} {pkg}: {req}")
            all_satisfied = all_satisfied and satisfied
        
        if all_satisfied:
            print(f"  ✅ PASS: pydantic {version} satisfies all requirements")
        else:
            print(f"  ❌ FAIL: pydantic {version} does not satisfy all requirements")
            all_valid_passed = False
    
    print("\n" + "=" * 70)
    print("Testing Invalid Versions (should fail)")
    print("=" * 70)
    
    all_invalid_failed = True
    for version in invalid_versions:
        print(f"\nTesting pydantic {version}:")
        
        # Check if it satisfies our constraint (it shouldn't)
        satisfies_ours = check_version_satisfies(version, our_constraint)
        
        if satisfies_ours:
            print(f"  ✗ ERROR: Should not satisfy our constraint but does!")
            all_invalid_failed = False
        else:
            print(f"  ✓ Correctly rejected by our constraint: {our_constraint}")
            
            # Show why it fails
            for pkg, req in requirements.items():
                if req == "any":
                    continue
                satisfied = check_version_satisfies(version, req)
                if not satisfied:
                    print(f"    - Fails {pkg} requirement: {req}")
    
    print("\n" + "=" * 70)
    print("Conclusion")
    print("=" * 70)
    
    if all_valid_passed and all_invalid_failed:
        print("\n✅ SUCCESS: The pydantic constraint is CORRECT!")
        print(f"\nThe constraint {our_constraint} will allow pip to install")
        print("pydantic 2.11.5 or higher (but less than 3.0.0), which satisfies:")
        print("  ✓ llama-index-workflows (>=2.11.5)")
        print("  ✓ llama-index-core (>=2.8.0)")
        print("  ✓ fastapi (<3.0.0)")
        print("  ✓ gradio (>=2.0)")
        print("  ✓ banks (any pydantic)")
        print("\nThe dependency conflict is RESOLVED!")
        return 0
    else:
        print("\n❌ FAILURE: The constraint has issues!")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

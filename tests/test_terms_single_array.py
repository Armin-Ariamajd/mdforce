"""
Test functions for individual force-field terms in `mdforce.terms_single_array.py`, evaluated using
functions in `mdforce.terms_single_simple`.
"""


# 3rd-party packages
import numpy as np

# Self
from mdforce import terms_single_simple as terms_simple
from mdforce import terms_single_array as terms_array


# Set up random number generator with seed to make sure testing results are consistent
random_gen = np.random.RandomState(1111)


def test_coulomb():
    """
    Test function for `mdforce.terms_single_array.coulomb`.
    """
    # Run the test 100 times
    for i in range(100):
        # Create sets of random parameters (in range [-1, 1))
        rand_vals = random_gen.random_sample(size=9) * 2 - 1
        q_i_x = rand_vals[0]
        q_i_y = rand_vals[1]
        q_i_z = rand_vals[2]
        q_j_x = rand_vals[3]
        q_j_y = rand_vals[4]
        q_j_z = rand_vals[5]
        c_i = rand_vals[6]
        c_j = rand_vals[7]
        k_e = rand_vals[8]
        # Calculate potential between particles 'i' and 'j', and the force on 'i' due to 'j',
        # using the already tested function in `terms_simple`
        f_i_x, f_i_y, f_i_z, e_ij = terms_simple.coulomb(
            q_i_x=q_i_x,
            q_i_y=q_i_y,
            q_i_z=q_i_z,
            q_j_x=q_j_x,
            q_j_y=q_j_y,
            q_j_z=q_j_z,
            c_i=c_i,
            c_j=c_j,
            k_e=k_e,
        )
        # Create equivalent arrays for testing the equivalent function in `terms_single_array`
        q_i = np.array([q_i_x, q_i_y, q_i_z])
        q_j = np.array([q_j_x, q_j_y, q_j_z])
        # Call the equivalent function in `terms_single_array`
        f_i_calc, e_ij_calc = terms_array.coulomb(q_i=q_i, q_j=q_j, c_i=c_i, c_j=c_j, k_e=k_e)
        # Verify that both functions' results are the same
        assert np.isclose(e_ij_calc, e_ij)
        assert np.isclose(f_i_calc[0], f_i_x)
        assert np.isclose(f_i_calc[1], f_i_y)
        assert np.isclose(f_i_calc[2], f_i_z)

        # Calculate potential between 'j' and 'i', and force on 'j', using the equivalent function
        f_j_calc, e_ji_calc = terms_array.coulomb(q_j, q_i, c_j, c_i, k_e)
        # Verify that the potential remains the same, and the force on 'j' is equal to the force on
        # 'i' multiplied with -1
        assert np.isclose(e_ji_calc, e_ij)
        assert np.isclose(f_j_calc[0], -f_i_x)
        assert np.isclose(f_j_calc[1], -f_i_y)
        assert np.isclose(f_j_calc[2], -f_i_z)
    return


def test_lennard_jones():
    """
    Test function for `mdforce.terms_single_array.lennard_jones`.
    """
    # Run the test 100 times
    for i in range(100):
        # Create sets of random parameters (in range [-1, 1))
        rand_vals = random_gen.random_sample(size=8) * 2 - 1
        q_i_x = rand_vals[0]
        q_i_y = rand_vals[1]
        q_i_z = rand_vals[2]
        q_j_x = rand_vals[3]
        q_j_y = rand_vals[4]
        q_j_z = rand_vals[5]
        a_ij = rand_vals[6]
        b_ij = rand_vals[7]
        # Calculate potential between particles 'i' and 'j', and the force on 'i' due to 'j',
        # using the already tested function in `terms_simple`
        f_i_x, f_i_y, f_i_z, e_ij = terms_simple.lennard_jones(
            q_i_x=q_i_x,
            q_i_y=q_i_y,
            q_i_z=q_i_z,
            q_j_x=q_j_x,
            q_j_y=q_j_y,
            q_j_z=q_j_z,
            a_ij=a_ij,
            b_ij=b_ij,
        )
        # Create equivalent arrays for testing the equivalent function in `terms_array`
        q_i = np.array([q_i_x, q_i_y, q_i_z])
        q_j = np.array([q_j_x, q_j_y, q_j_z])
        # Call the equivalent function in `terms_array`
        f_i_calc, e_ij_calc = terms_array.lennard_jones(q_i=q_i, q_j=q_j, a_ij=a_ij, b_ij=b_ij)
        # Verify that both functions' results are the same
        assert np.isclose(e_ij_calc, e_ij)
        assert np.isclose(f_i_calc[0], f_i_x)
        assert np.isclose(f_i_calc[1], f_i_y)
        assert np.isclose(f_i_calc[2], f_i_z)
        # Calculate potential between 'j' and 'i', and force on 'j', using the equivalent function
        f_j_calc, e_ji_calc = terms_array.lennard_jones(q_i=q_j, q_j=q_i, a_ij=a_ij, b_ij=b_ij)
        # Verify that the potential remains the same, and the force on 'j' is equal to the force on
        # 'i' multiplied with -1
        assert np.isclose(e_ji_calc, e_ij)
        assert np.isclose(f_j_calc[0], -f_i_x)
        assert np.isclose(f_j_calc[1], -f_i_y)
        assert np.isclose(f_j_calc[2], -f_i_z)
    return


def test_bond_vibration_harmonic():
    """
    Test function for `mdforce.terms_single_array.bond_vibration_harmonic`.
    """
    # Run the test 100 times
    for i in range(100):
        # Create sets of random parameters (in range [-1, 1))
        rand_vals = random_gen.random_sample(size=8) * 2 - 1
        q_i_x = rand_vals[0]
        q_i_y = rand_vals[1]
        q_i_z = rand_vals[2]
        q_j_x = rand_vals[3]
        q_j_y = rand_vals[4]
        q_j_z = rand_vals[5]
        d0 = rand_vals[6]
        k_b = rand_vals[7]
        # Calculate potential between particles 'i' and 'j', and the force on 'i' due to 'j',
        # using the already tested function in `terms_simple`
        f_i_x, f_i_y, f_i_z, e_ij = terms_simple.bond_vibration_harmonic(
            q_i_x=q_i_x,
            q_i_y=q_i_y,
            q_i_z=q_i_z,
            q_j_x=q_j_x,
            q_j_y=q_j_y,
            q_j_z=q_j_z,
            d0=d0,
            k_b=k_b,
        )
        # Create equivalent arrays for testing the equivalent function in `terms_array`
        q_i = np.array([q_i_x, q_i_y, q_i_z])
        q_j = np.array([q_j_x, q_j_y, q_j_z])
        # Call the equivalent function in `terms_array`
        f_i_calc, e_ij_calc = terms_array.bond_vibration_harmonic(q_i=q_i, q_j=q_j, d0=d0, k_b=k_b)
        # Verify that both functions' results are the same
        assert np.isclose(e_ij_calc, e_ij)
        assert np.isclose(f_i_calc[0], f_i_x)
        assert np.isclose(f_i_calc[1], f_i_y)
        assert np.isclose(f_i_calc[2], f_i_z)

        # Calculate potential between 'j' and 'i', and force on 'j', using the equivalent function
        f_j_calc, e_ji_calc = terms_array.bond_vibration_harmonic(q_i=q_j, q_j=q_i, d0=d0, k_b=k_b)
        # Verify that the potential remains the same, and the force on 'j' is equal to the force on
        # 'i' multiplied with -1
        assert np.isclose(e_ji_calc, e_ij)
        assert np.isclose(f_j_calc[0], -f_i_x)
        assert np.isclose(f_j_calc[1], -f_i_y)
        assert np.isclose(f_j_calc[2], -f_i_z)
    return


def test_angle_vibration_harmonic():
    """
    Test function for `mdforce.terms_single_array.angle_vibration_harmonic`.
    """
    # Run the test 100 times
    for i in range(100):
        # Create sets of random parameters (in range [-1, 1))
        rand_vals = random_gen.random_sample(size=11) * 2 - 1
        q_i_x = rand_vals[0]
        q_i_y = rand_vals[1]
        q_i_z = rand_vals[2]
        q_j_x = rand_vals[3]
        q_j_y = rand_vals[4]
        q_j_z = rand_vals[5]
        q_k_x = rand_vals[6]
        q_k_y = rand_vals[7]
        q_k_z = rand_vals[8]
        angle0 = rand_vals[9]
        k_a = rand_vals[10]
        # Calculate potential between particles 'i' and 'j', and the force on 'i' due to 'j',
        # using the already tested function in `terms_simple`
        (
            f_i_x,
            f_i_y,
            f_i_z,
            f_j_x,
            f_j_y,
            f_j_z,
            f_k_x,
            f_k_y,
            f_k_z,
            e_ijk,
        ) = terms_simple.angle_vibration_harmonic(
            q_i_x=q_i_x,
            q_i_y=q_i_y,
            q_i_z=q_i_z,
            q_j_x=q_j_x,
            q_j_y=q_j_y,
            q_j_z=q_j_z,
            q_k_x=q_k_x,
            q_k_y=q_k_y,
            q_k_z=q_k_z,
            angle0=angle0,
            k_a=k_a,
        )
        # Create equivalent arrays for testing the equivalent function in `terms_array`
        q_i = np.array([q_i_x, q_i_y, q_i_z])
        q_j = np.array([q_j_x, q_j_y, q_j_z])
        q_k = np.array([q_k_x, q_k_y, q_k_z])
        # Call the equivalent function in `terms_array`
        f_i_calc, f_j_calc, f_k_calc, e_ijk_calc = terms_array.angle_vibration_harmonic(
            q_i=q_i, q_j=q_j, q_k=q_k, angle0=angle0, k_a=k_a
        )
        # Verify that both functions' results are the same
        assert np.isclose(e_ijk_calc, e_ijk)
        assert np.isclose(f_i_calc[0], f_i_x)
        assert np.isclose(f_i_calc[1], f_i_y)
        assert np.isclose(f_i_calc[2], f_i_z)
        assert np.isclose(f_j_calc[0], f_j_x)
        assert np.isclose(f_j_calc[1], f_j_y)
        assert np.isclose(f_j_calc[2], f_j_z)
        assert np.isclose(f_k_calc[0], f_k_x)
        assert np.isclose(f_k_calc[1], f_k_y)
        assert np.isclose(f_k_calc[2], f_k_z)

        # Calculate potential between 'k', 'j' and 'i', and force on each of them, using the
        # equivalent function
        f_k_calc2, f_j_calc2, f_i_calc2, e_ijk_calc2 = terms_array.angle_vibration_harmonic(
            q_i=q_k, q_j=q_j, q_k=q_i, angle0=angle0, k_a=k_a
        )
        # Verify that swapping 'i' and 'k' gives the same potential and same force for 'j' (i.e.
        # the midlle particle), but swaps the forces of 'i' and 'k'
        assert np.all(np.isclose(e_ijk_calc2, e_ijk_calc))
        assert np.all(np.isclose(f_j_calc2, f_j_calc))
        assert np.all(np.isclose(f_k_calc2, f_k_calc))
        assert np.all(np.isclose(f_i_calc2, f_i_calc))
    return

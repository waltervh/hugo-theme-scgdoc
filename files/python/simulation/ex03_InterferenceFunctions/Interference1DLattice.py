"""
Long boxes on a 1D lattice
"""
import numpy
import bornagain as ba
from bornagain import deg, angstrom, nm


def get_sample():
    """
    Returns a sample with a grating on a substrate.
    The structure is modelled by infinitely long boxes forming a 1D lattice.
    """
    # defining materials
    m_ambience = ba.HomogeneousMaterial("Air", 0.0, 0.0)
    m_substrate = ba.HomogeneousMaterial("Substrate", 6e-6, 2e-8)
    m_particle = ba.HomogeneousMaterial("Particle", 6e-4, 2e-8)

    # collection of particles
    lattice_length = 30.0*nm
    lattice_rotation_angle = 0.0*deg
    interference = ba.InterferenceFunction1DLattice(
        lattice_length, lattice_rotation_angle)
    pdf = ba.FTDecayFunction1DCauchy(20./2./numpy.pi*nm)
    interference.setDecayFunction(pdf)

    box_ff = ba.FormFactorBox(1000*nm, 10*nm, 15.0*nm)
    box = ba.Particle(m_particle, box_ff)
    transform = ba.RotationZ(25.0*deg)
    particle_layout = ba.ParticleLayout()
    particle_layout.addParticle(box, 1.0, ba.kvector_t(0.0, 0.0, 0.0), transform)
    particle_layout.setInterferenceFunction(interference)

    # assembling the sample
    air_layer = ba.Layer(m_ambience)
    air_layer.addLayout(particle_layout)
    substrate_layer = ba.Layer(m_substrate)

    multi_layer = ba.MultiLayer()
    multi_layer.addLayer(air_layer)
    multi_layer.addLayer(substrate_layer)
    return multi_layer


def get_simulation():
    """
    Create and return GISAXS simulation with beam and detector defined
    """
    simulation = ba.GISASSimulation()
    simulation.setDetectorParameters(200, -1.0*deg, 1.0*deg,
                                     200, 0.0*deg, 2.0*deg)
    simulation.setBeamParameters(24.0*angstrom, 0.2*deg, 0.0*deg)
    return simulation


def run_simulation():
    """
    Runs simulation and returns intensity map.
    """
    simulation = get_simulation()
    simulation.setSample(get_sample())
    simulation.runSimulation()
    return simulation.result()


if __name__ == '__main__':
    result = run_simulation()
    ba.plot_simulation_result(result)

# -*- coding: utf-8 -*-

# Copyright (c) 2016-2019 by University of Kassel and Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.


import os

import numpy as np
import pytest

import pandapower as pp
import pandapower.networks as nw
from pandapower.estimation import StateEstimation, estimate
from pandapower.estimation.util import add_virtual_meas_from_loadflow, add_virtual_pmu_meas_from_loadflow
from copy import deepcopy


def test_pmu_four_bus():
#    net = nw.simple_four_bus_system()
#    net = nw.case9()
    net = nw.case30()

    net.trafo.shift_degree = 0
    pp.runpp(net)
    add_virtual_pmu_meas_from_loadflow(net)
#    net.measurement = net.measurement.loc[net.measurement.measurement_type!="ia"]
    
    estimate(net)
    pp.runpp(net)
    assert np.allclose(net.res_bus.vm_pu, net.res_bus_est.vm_pu, atol=1e-2)
    assert np.allclose(net.res_bus.va_degree, net.res_bus_est.va_degree, atol=1e-1)  


def test_pmu_with_trafo3w():
    net = pp.create_empty_network()

    bus_slack = pp.create_bus(net, vn_kv=110)
    pp.create_ext_grid(net, bus=bus_slack)

    bus_20_1 = pp.create_bus(net, vn_kv=20,name="b")
    pp.create_sgen(net, bus=bus_20_1, p_mw=0.03, q_mvar=0.02)

    bus_10_1 = pp.create_bus(net, vn_kv=10)
    pp.create_sgen(net, bus=bus_10_1, p_mw=0.02, q_mvar=0.02)

    bus_10_2 = pp.create_bus(net, vn_kv=10)
    pp.create_load(net, bus=bus_10_2, p_mw=0.06, q_mvar=0.01)
    pp.create_line(net, from_bus=bus_10_1, to_bus=bus_10_2, std_type="149-AL1/24-ST1A 10.0", length_km=2)

    pp.create_transformer3w(net, bus_slack, bus_20_1, bus_10_1, std_type="63/25/38 MVA 110/20/10 kV")

    pp.runpp(net)
    add_virtual_pmu_meas_from_loadflow(net)

    estimate(net)
    pp.runpp(net)
    assert np.allclose(net.res_bus.vm_pu, net.res_bus_est.vm_pu, atol=1e-2)
    assert np.allclose(net.res_bus.va_degree, net.res_bus_est.va_degree, atol=1e-1)  


if __name__ == '__main__':
#    pytest.main([__file__, "-xs"])

    net = nw.case9()
#    net = nw.case14()
    
    net.trafo.shift_degree = 0
    pp.runpp(net)
    add_virtual_pmu_meas_from_loadflow(net)
    net.measurement = net.measurement.loc[net.measurement.measurement_type!="va"]
#    net.measurement = net.measurement.loc[net.measurement.measurement_type!="ia"]
#    net.measurement = net.measurement.loc[net.measurement.measurement_type!="i"]
#    net.measurement = net.measurement.reset_index()
    
    estimate(net)
    pp.runpp(net)
    assert np.allclose(net.res_bus.vm_pu, net.res_bus_est.vm_pu, atol=1e-2)
    assert np.allclose(net.res_bus.va_degree, net.res_bus_est.va_degree, atol=3e-1)  
class Parameters:
    # Parameters
    alpha=24*10**6;#bits
    T=3600;#seconds
    sigma=1;#Time slot (in seconds)
    C=1000;#cycle per bit
    f=2*10**9;#ycle per second
    G0=-50;#dB
    H=100;#meters
    N0=-130;#dBm/Hz
    B=20*10**6;#Hz
    Pm=35;#dBm
    Qm=6;#seconds
    RoadLength=5000;
    V_max = 20; # m/sec;
    U = 120; # m/sec
    v_0 = 4.03;#Mean rotor induced velocity in hover
    c_0 = 0.6;#Fuselage drag ratio
    epsilon = 1.225; #kg/m^3
    r = 0.05;#Rotor solidity
    A = 0.503; #m^2
    k = 10**(-28); #coefficient
    UAVSpeed=20;
    #energy parameters 
    b_sigma = 0.012;
    b_k = 0.1;
    b_W = 20;
    b_p = 1.225;
    b_s = 0.05;
    b_A = 0.503;
    b_omega = 300;
    b_R = 0.4;
    E_max=68*(10**3);#joule


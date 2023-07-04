Include "Vector.geo";

Macro RotatePoint
    pointId = Arguments[0];
    angle = Arguments[1];
    center[] = Arguments[{2:4}];
    Rotate {{0, 0, 1}, {center[0], center[1], center[2]}, angle}
    {
        Point{pointId};
    }
Return

Macro RotateAirfoilPoint
    // rotates pointId about quarter-chord.
    Arguments[1] *= -1.0;
    Arguments[{2:4}] = {0.25 , 0, 0};
    Call RotatePoint;
Return


Macro TowBendsAirfoil
    aoa = Arguments[0] * Pi / 180;
    leBendHeight = Arguments[1];
    leBendLocation = Arguments[2];
    teBendHeight = Arguments[3];
    teBendLocation = Arguments[4];
    thickness = Arguments[5];
    lc = Arguments[6];

    allPoints[] = {};

    Point(ce++) = {0, 0, 0, lc};
    leCenter = ce - 1;
    Point(ce++) = {leBendLocation, leBendHeight - thickness, 0, lc};
    lePeakCenter = ce - 1;
    Point(ce++) = {teBendLocation, teBendHeight - thickness, 0, lc};
    tePeakCenter = ce - 1;
    Point(ce++) = {1, 0, 0, lc};
    teCenter = ce - 1;
    allPoints[] += {leCenter, lePeakCenter, tePeakCenter, teCenter};

    Arguments[] = {Point{leCenter}, Point{lePeakCenter}}; Call Vector;
    leTolePeak[] = Results[{0:2}];
    Arguments[] = {1, 0, 0, leTolePeak[]}; Call Angle;
    frontAngle = Results[0];
    Arguments[] = {Point{tePeakCenter}, Point{lePeakCenter}}; Call Vector;
    tePeakTolePeak[] = Results[{0:2}];
    Arguments[] = {tePeakTolePeak, leBendLocation - teBendLocation, teBendHeight - thickness, 0}; Call Angle;
    middleAngle = Results[0];
    Arguments[] = {Point{teCenter}, Point{tePeakCenter}}; Call Vector;
    teTotePeak[] = Results[{0:2}];
    Arguments[] = {teTotePeak[], -1, 0, 0}; Call Angle;
    backAngle = Results[0];
    Printf("INFO: bend angle: %f", 90 - frontAngle * 180 / Pi + 90 - backAngle * 180 / Pi);

    lePoints[] = {};
    Point(ce++) = {0, 0.5 * thickness, 0, lc};
    lePoints[] += ce - 1;
    Point(ce++) = {0, -0.5 * thickness, 0, lc};
    lePoints[] += ce - 1;
    For p In {0:1}
        Arguments[] = {lePoints[p], frontAngle, Point{leCenter}}; Call RotatePoint;
    EndFor
    allPoints[] += lePoints[];

    tePoints[] = {};
    Point(ce++) = {1, 0.5 * thickness, 0, lc};
    tePoints[] += ce - 1;
    Point(ce++) = {1, -0.5 * thickness, 0, lc};
    tePoints[] += ce - 1;
    For p In {0:1}
        Arguments[] = {tePoints[p], -backAngle, Point{teCenter}}; Call RotatePoint;
    EndFor
    allPoints[] += tePoints[];

    leBendPoints[] = {};
    Point(ce++) = {leBendLocation, leBendHeight - 1.5 * thickness, 0, 5 * lc};
    leBendPoints[] += ce - 1;
    Point(ce++) = {leBendLocation - 0.5 * thickness, leBendHeight - thickness, 0, lc};
    leBendPoints[] += ce - 1;
    Arguments[] = {ce - 1, -(0.5 * Pi - frontAngle), Point{lePeakCenter}}; Call RotatePoint;
    Point(ce++) = {leBendLocation + 0.5 * thickness, leBendHeight - thickness, 0, lc};
    leBendPoints[] += ce - 1;
    Arguments[] = {ce - 1,  middleAngle, Point{lePeakCenter}}; Call RotatePoint;
    allPoints[] += leBendPoints[];

    teBendPoints[] = {};
    Point(ce++) = {teBendLocation, teBendHeight - 1.5 * thickness, 0, 5 * lc};
    teBendPoints[] += ce - 1;
    Point(ce++) = {teBendLocation - 0.5 * thickness, teBendHeight - thickness, 0, lc};
    teBendPoints[] += ce - 1;
    Arguments[] = {ce - 1, - middleAngle, Point{tePeakCenter}}; Call RotatePoint;
    Point(ce++) = {teBendLocation + 0.5 * thickness, teBendHeight - thickness, 0, lc};
    teBendPoints[] += ce - 1;
    Arguments[] = {ce - 1, (0.5 * Pi - backAngle), Point{tePeakCenter}}; Call RotatePoint;
    allPoints[] += teBendPoints[];

    For p In {0:#allPoints[] - 1}
        Arguments[] = {allPoints[p], aoa};
        Call RotateAirfoilPoint;
    EndFor

    loopLines[] = {};
    Line(ce++) = {teCenter, tePoints[0]};
    loopLines[] += ce - 1;
    Line(ce++) = {tePoints[0], teBendPoints[2]};
    loopLines[] += ce - 1;
    Circle(ce++) = {teBendPoints[2], tePeakCenter, teBendPoints[1]};
    loopLines[] += ce - 1;
    Line(ce++) = {teBendPoints[1], leBendPoints[2]};
    loopLines[] += ce - 1;
    Circle(ce++) = {leBendPoints[2], lePeakCenter, leBendPoints[1]};
    loopLines[] += ce - 1;
    Line(ce++) = {leBendPoints[1], lePoints[0]};
    loopLines[] += ce - 1;
    Line(ce++) = {lePoints[0], leCenter};
    loopLines[] += ce - 1;
    Line(ce++) = {leCenter, lePoints[1]};
    loopLines[] += ce - 1;
    Line(ce++) = {lePoints[1], leBendPoints[0]};
    loopLines[] += ce - 1;
    Line(ce++) = {leBendPoints[0], teBendPoints[0]};
    loopLines[] += ce - 1;
    Line(ce++) = {teBendPoints[0], tePoints[1]};
    loopLines[] += ce - 1;
    Line(ce++) = {tePoints[1], teCenter};
    loopLines[] += ce - 1;

    Line Loop(ce++) = loopLines[];
    Results[0] = ce - 1;    
Return

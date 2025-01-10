# UAV_BAT
### Simulator
Car arrivals and task generation made in this script.
Corresponding simulation values saved in .npy files in the folder data.
- allTask

    this is a time matrix. If the value is 0 there are no task generated at that moment. values different than 0 shows which car generated that task.

- CAVs

    this is a object matrix. It stores the cav objects.

- leavingTimes

    has the shape of the number of total cars. Each index show in which time index does the corresponding vehicle left the road.

### Objects
#### CAV
It stores the values mentioned below
- Speed
- Entering Time
- Position Vector
- Leaving Time
- Task Times
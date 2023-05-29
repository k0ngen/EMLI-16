# EMLI 16

## Crontab
The WiFi hotspot is started on every boot by 
```
@reboot sleep 10 && /home/pi/EMLI-16/Scripts/start_hotspot.sh
```
which has been inserted into the crontab of root.

The ROS2 nodes is started on every boot by
```
@reboot sleep 10 && /home/pi/EMLI-16/Scripts/start_ros2_nodes.sh
```
which has been inserted into the crontab of root.

The hourly and daily waterings are run every 10 minutes and every hour by
```
*/10 * * * * /home/pi/EMLI-16/Scripts/water_on_condition.sh
1 */12 * * * /home/pi/EMLI-16/Scripts/water_daily.sh
``` 
which has been inserted into the crontab of root.

The logging of system data is done by 
```
*/10 * * * * /home/pi/EMLI-16/Scripts/log_system_state.sh
``` 
which has been inserted into the crontab of root.

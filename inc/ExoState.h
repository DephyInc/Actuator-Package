#ifdef __cplusplus
  extern "C" {
#endif

#define MAX_STRING_LENGTH 32

/* Structure that holds a deserialized GenericVariables-message. */
struct GenericVariables {
    signed long _gv0;
    signed long _gv1;
    signed long _gv2;
    signed long _gv3;
    signed long _gv4;
    signed long _gv5;
    signed long _gv6;
    signed long _gv7;
    signed long _gv8;
    signed long _gv9;
};

/* Structure that holds a deserialized ImuData-message. */
struct ImuData {
    signed long _accelx;
    signed long _accely;
    signed long _accelz;
    signed long _gyrox;
    signed long _gyroy;
    signed long _gyroz;
};

/* Structure that holds a deserialized MotorData-message. */
struct MotorData {
    signed long _motor_angle;
    signed long _motor_velocity;
    signed long _motor_acceleration;
    signed long _motor_current;
    signed long _motor_voltage;
};

/* Structure that holds a deserialized BatteryData-message. */
struct BatteryData {
    unsigned long _battery_voltage;
    signed long _battery_current;
    signed long _battery_temperature;
};

/* Structure that holds a deserialized ManageState-message. */
struct ManageState {
    unsigned long _status;
    int _software_version_len;
    char _software_version[MAX_STRING_LENGTH];
    struct ImuData _imu;
    signed long _ankle_angle;
    signed long _ankle_angle_velocity;
};

/* Structure that holds a deserialized ExecuteState-message. */
struct ExecuteState {
    unsigned long _status;
    struct MotorData _motor_data;
    int _software_version_len;
    char _software_version[MAX_STRING_LENGTH];
};

/* Structure that holds a deserialized RegulateState-message. */
struct RegulateState {
    unsigned long _status;
    struct BatteryData _battery;
    int _software_version_len;
    char _software_version[MAX_STRING_LENGTH];
};

/* Structure that holds a deserialized ExoState-message. */
struct ExoState {
    unsigned long _timestamp;
    unsigned long _board_id;
    struct ManageState _manage;
    struct ExecuteState _execute;
    struct RegulateState _regulate;
    struct GenericVariables _genvars;
};

#ifdef __cplusplus
}
#endif

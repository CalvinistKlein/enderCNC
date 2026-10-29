/**
 * ============================================================================
 * Marlin 2.1.x CNC Configuration Patch for Creality Ender 3 (V4.2.2 / V4.2.7)
 * Target MCU: STM32F103RET6 (32-bit)
 * Machine Spec: RepStrap Zero-Cut 10.5" x 11.0" x 3.5" (High-Deck) / 2.0" (Low-Deck)
 * Spindle: Harbor Freight Drill Master 62659 1/4" Trim Router via SSR on PA1 (HE0)
 * ============================================================================
 */

#pragma once

// 1. Disable Extruders, Thermistors & Thermal Runaway Protection
#define EXTRUDERS 0
#define TEMP_SENSOR_0 0
#define TEMP_SENSOR_BED 0
#undef THERMAL_PROTECTION_HOTENDS
#undef THERMAL_PROTECTION_BED

// 2. Working Travel Envelope (10.5" X x 11.0" Y x 3.5" Z in mm)
#define X_BED_SIZE 266.7   // 10.50 inches
#define Y_BED_SIZE 279.4   // 11.00 inches
#define Z_MAX_POS   88.9   //  3.50 inches (High-Deck Mode; set 50.8 for Low-Deck)

// 3. Motion Steps/mm, Max Feedrates (mm/s), and Cutting Accelerations (mm/s^2)
#define DEFAULT_AXIS_STEPS_PER_UNIT   { 80.0, 80.0, 400.0 }
#define DEFAULT_MAX_FEEDRATE          { 60, 60, 12 }
#define DEFAULT_MAX_ACCELERATION      { 400, 400, 80 }
#define DEFAULT_ACCELERATION          300
#define DEFAULT_JERK                  2.0

// 4. Spindle Relay Output on Hotend MOSFET Terminal (HE0 = PA1)
#define SPINDLE_FEATURE
#define SPINDLE_LASER_USE_PWM false
#define SPINDLE_LASER_ENA_PIN PA1
#define SPINDLE_LASER_ACTIVE_STATE HIGH
#define SPINDLE_CHANGE_DIR false
#define SPINDLE_STOP_ON_ERROR

// 5. CNC Work Coordinate Offsets (G54-G59) & Carbide Touch-Plate Probing (G38.2 on PA7)
#define CNC_WORKSPACE_PLANES
#define CNC_COORDINATE_SYSTEMS
#define G38_PROBE_TARGET
#define Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN
#define Z_MIN_PROBE_ENDSTOP_INVERTING true

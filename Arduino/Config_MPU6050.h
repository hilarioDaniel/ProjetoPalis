/* 
 * File:   Config_MPU6050.h
 * Author: RODRIGO
 *
 * Created on 1 de Abril de 2020, 16:23
 */

#ifndef CONFIG_MPU6050_H
#define	CONFIG_MPU6050_H

#include <Wire.h>
#include<Arduino.h>


#define FIFO_CORRUPTION_CHECK
#ifdef FIFO_CORRUPTION_CHECK
  #define QUAT_ERROR_THRESH       (1L<<24)
  #define QUAT_MAG_SQ_NORMALIZED  (1L<<28)
  #define QUAT_MAG_SQ_MIN         (QUAT_MAG_SQ_NORMALIZED - QUAT_ERROR_THRESH)
  #define QUAT_MAG_SQ_MAX         (QUAT_MAG_SQ_NORMALIZED + QUAT_ERROR_THRESH)
#endif

#define TAP_X               (0x01)
#define TAP_Y               (0x02)
#define TAP_Z               (0x04)
#define TAP_XYZ             (0x07)

#define INV_X_GYRO      (0x40)
#define INV_Y_GYRO      (0x20)
#define INV_Z_GYRO      (0x10)
#define INV_XYZ_GYRO    (INV_X_GYRO | INV_Y_GYRO | INV_Z_GYRO)
#define INV_XYZ_ACCEL   (0x08)
#define INV_XYZ_COMPASS (0x01)
#define INV_WXYZ_QUAT   (0x100)

#define DMP_FEATURE_TAP             (0x001)
#define DMP_FEATURE_ANDROID_ORIENT  (0x002)
#define DMP_FEATURE_LP_QUAT         (0x004)
#define DMP_FEATURE_PEDOMETER       (0x008)
#define DMP_FEATURE_6X_LP_QUAT      (0x010)
#define DMP_FEATURE_GYRO_CAL        (0x020)
#define DMP_FEATURE_SEND_RAW_ACCEL  (0x040)
#define DMP_FEATURE_SEND_RAW_GYRO   (0x080)
#define DMP_FEATURE_SEND_CAL_GYRO   (0x100)

class InertialSensor 
{
    private:
        static uint8_t uDevAddress;
        /* Clock sources. */
        enum clock_sel_e 
        {
            INV_CLK_INTERNAL = 0,
            INV_CLK_PLL,
            NUM_CLK
        };
        /* Low-power accel wakeup rates. */
        enum lp_accel_rate_e {
       
            INV_LPA_1_25HZ,
            INV_LPA_5HZ,
            INV_LPA_20HZ,
            INV_LPA_40HZ
        
        };
        /* Filter configurations. */
        enum lpf_e {
            INV_FILTER_256HZ_NOLPF2 = 0,
            INV_FILTER_188HZ,
            INV_FILTER_98HZ,
            INV_FILTER_42HZ,
            INV_FILTER_20HZ,
            INV_FILTER_10HZ,
            INV_FILTER_5HZ,
            INV_FILTER_2100HZ_NOLPF,
            NUM_FILTER
        };
        
        /* Full scale ranges. */
        enum gyro_fsr_e {
            INV_FSR_250DPS = 0,
            INV_FSR_500DPS,
            INV_FSR_1000DPS,
            INV_FSR_2000DPS,
            NUM_GYRO_FSR
        };
        /* Full scale ranges. */
        enum accel_fsr_e {
            INV_FSR_2G = 0,
            INV_FSR_4G,
            INV_FSR_8G,
            INV_FSR_16G,
            NUM_ACCEL_FSR
        };
        

    public:
                
        //static int AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
        //static int regXaXgTest, regYaYgTest,regZaZgTest,regXaYaZaTest;

        /* Hardware registers needed by driver. */
        struct gyro_reg_s {
        unsigned char who_am_i;
        unsigned char rate_div;
        unsigned char lpf;
        unsigned char prod_id;
        unsigned char user_ctrl;
        unsigned char fifo_en;
        unsigned char gyro_cfg;
        unsigned char accel_cfg;
        /*unsigned char accel_cfg2;*/
        /*unsigned char lp_accel_odr;*/
        unsigned char motion_thr;
        unsigned char motion_dur;
        unsigned char fifo_count_h;
        unsigned char fifo_r_w;
        unsigned char raw_gyro;
        unsigned char raw_accel;
        unsigned char temp;
        unsigned char int_enable;
        unsigned char dmp_int_status;
        unsigned char int_status;
        /*unsigned char accel_intel;*/
        unsigned char pwr_mgmt_1;
        unsigned char pwr_mgmt_2;
        unsigned char int_pin_cfg;
        unsigned char mem_r_w;
        unsigned char accel_offs;
        unsigned char i2c_mst;
        unsigned char bank_sel;
        unsigned char mem_start_addr;
        unsigned char prgm_start_h;
        };
        /* Information specific to a particular device. */
        struct hw_s {
            unsigned char addr;
            unsigned short max_fifo;
            unsigned char num_reg;
            unsigned short temp_sens;
            short temp_offset;
            unsigned short bank_size;
        };
        /* When entering motion interrupt mode, the driver keeps track of the
         * previous state so that it can be restored at a later time.
         * TODO: This is tacky. Fix it.
         */
          struct motion_int_cache_s {
              unsigned short gyro_fsr;
              unsigned char accel_fsr;
              unsigned short lpf;
              unsigned short sample_rate;
              unsigned char sensors_on;
              unsigned char fifo_sensors;
              unsigned char dmp_on;
          };
        /* Cached chip configuration data.
         * TODO: A lot of these can be handled with a bitmask.
         */
        struct chip_cfg_s {
            /* Matches gyro_cfg >> 3 & 0x03 */
            unsigned char gyro_fsr;
            /* Matches accel_cfg >> 3 & 0x03 */
            unsigned char accel_fsr;
            /* Enabled sensors. Uses same masks as fifo_en, NOT pwr_mgmt_2. */
            unsigned char sensors;
            /* Matches config register. */
            unsigned char lpf;
            unsigned char clk_src;
            /* Sample rate, NOT rate divider. */
            unsigned short sample_rate;
            /* Matches fifo_en register. */
            unsigned char fifo_enable;
            /* Matches int enable register. */
            unsigned char int_enable;
            /* 1 if devices on auxiliary I2C bus appear on the primary. */
            unsigned char bypass_mode;
            /* 1 if half-sensitivity.
             * NOTE: This doesn't belong here, but everything else in hw_s is const,
             * and this allows us to save some precious RAM.
             */
            unsigned char accel_half;
            /* 1 if device in low-power accel-only mode. */
            unsigned char lp_accel_mode;
            /* 1 if interrupts are only triggered on motion events. */
            unsigned char int_motion_only;
            struct motion_int_cache_s cache;
            /* 1 for active low interrupts. */
            unsigned char active_low_int;
            /* 1 for latched interrupts. */
            unsigned char latched_int;
            /* 1 if DMP is enabled. */
            unsigned char dmp_on;
            /* Ensures that DMP will only be loaded once. */
            unsigned char dmp_loaded;
            /* Sampling rate used when DMP is enabled. */
            unsigned short dmp_sample_rate;
            };
            /* Information for self-test. */
            struct test_s {
                unsigned long gyro_sens;
                unsigned long accel_sens;
                unsigned char reg_rate_div;
                unsigned char reg_lpf;
                unsigned char reg_gyro_fsr;
                unsigned char reg_accel_fsr;
                unsigned short wait_ms;
                unsigned char packet_thresh;
                float min_dps;
                float max_dps;
                float max_gyro_var;
                float min_g;
                float max_g;
                float max_accel_var;
             };

              /* Gyro driver state variables. */
              struct gyro_state_s {
              const struct gyro_reg_s *reg;
              const struct hw_s *hw;
              const struct test_s *test;
              struct chip_cfg_s chip_cfg;
              //const struct test_s *test;
              };

              struct rx_s {
                unsigned char header[3];
                unsigned char cmd;
              };
              struct hal_s {
                  unsigned char sensors;
                  unsigned char dmp_on;
                  unsigned char wait_for_tap;
                  volatile unsigned char new_gyro;
                  unsigned short report;
                  unsigned short dmp_features;
                  unsigned char motion_int_mode;
                  struct rx_s rx;
              };
              
              struct dmp_s {
                void (*tap_cb)(unsigned char count, unsigned char direction);
                void (*android_orient_cb)(unsigned char orientation);
                unsigned short orient;
                unsigned short feature_mask;
                unsigned short fifo_rate;
                unsigned char packet_length;
            };


    public:
        InertialSensor();
        //void initDevice(void);
        //void initReadDevice(void);
        //void initReadDeviceForFactoryTrim(void);
        //void read3Ac3Gy(void);
        //void readRegForFT(void);
        void initSystemDMP(void);
        void getDataFromProgMem(unsigned short sizeBuffer,unsigned short startIndex, const unsigned char *data,unsigned char *progBuffer);
        void upDateGyroStatus(void);
        void processDMP(void);
        void initCtrPointers(int var);
        void testaPonteiroFuncao(void);
        /* Set up APIs */
        int mpu_init(void);//(struct int_param_s *int_param);
        //int mpu_init_slave(void);
        int mpu_set_bypass(unsigned char bypass_on);
        /* Configuration APIs */
        int mpu_set_gyro_fsr(unsigned short fsr);
        int mpu_set_accel_fsr(unsigned char fsr);
        int mpu_set_lpf(unsigned short lpf);
        int mpu_set_sample_rate(unsigned short rate);
        int mpu_lp_accel_mode(unsigned short rate);
        int mpu_set_int_latched(unsigned char enable);
        int mpu_configure_fifo(unsigned char sensors);
        //static int set_int_enable(unsigned char enable);
        int set_int_enable(unsigned char enable);
        int mpu_reset_fifo(void);
        int mpu_set_sensors(unsigned char sensors);
        int mpu_get_sample_rate(unsigned short *rate);
        int mpu_get_gyro_fsr(unsigned short *fsr);
        int mpu_get_accel_fsr(unsigned char *fsr);
        int mpu_set_dmp_state(unsigned char enable);
        int mpu_set_gyro_bias_reg(long * gyro_bias);
        int mpu_read_6050_accel_bias(long *accel_bias);
        int mpu_read_6500_gyro_bias(long *gyro_bias);
        int mpu_get_lpf(unsigned short *lpf);
        int mpu_get_fifo_config(unsigned char *sensors);
        int mpu_set_accel_bias_6050_reg(const long *accel_bias);
        
        /* Data getter/setter APIs */
        int mpu_write_mem(unsigned short mem_addr, unsigned short length,unsigned char *data);
        int mpu_load_firmware(unsigned short length, const unsigned char *firmware,unsigned short start_addr, unsigned short sample_rate);
        int mpu_read_mem(unsigned short mem_addr, unsigned short length, unsigned char *data);
        /* Set up functions. */
        int dmp_load_motion_driver_firmware(void);
        int dmp_set_fifo_rate(unsigned short rate);
        int dmp_set_orientation(unsigned short orient);
        int dmp_enable_feature(unsigned short mask);
        /* Tap functions. */
        int dmp_register_tap_cb(void (*func)(unsigned char, unsigned char));
        int dmp_set_tap_thresh(unsigned char axis, unsigned short thresh);
        int dmp_set_tap_axes(unsigned char axis);
        int dmp_set_tap_count(unsigned char min_taps);
        int dmp_set_tap_time(unsigned short time);
        int dmp_set_tap_time_multi(unsigned short time);
        int dmp_set_shake_reject_thresh(long sf, unsigned short thresh);
        int dmp_set_shake_reject_time(unsigned short time);
        int dmp_set_shake_reject_timeout(unsigned short time);
        /* Android orientation functions. */
        int dmp_register_android_orient_cb(void (*func)(unsigned char));
        /* DMP gyro calibration functions. */
        int dmp_enable_gyro_cal(unsigned char enable);
        /* LP quaternion functions. */
        int dmp_enable_lp_quat(unsigned char enable);
        int dmp_enable_6x_lp_quat(unsigned char enable);
        /* Read function. This function should be called whenever the MPU interrupt is
         * detected.
         */
        int dmp_read_fifo(short *gyro, short *accel, long *quat,unsigned long *timestamp, short *sensors, unsigned char *more);
        /* Data getter/setter APIs */
        int mpu_run_self_test(long *gyro, long *accel);
        int mpu_read_fifo_stream(unsigned short length, unsigned char *data,unsigned char *more);
        /////////////////
        //static inline void run_self_test(void);
        void run_self_test(void);
        /////inv_mpu.c 
        //static int get_st_biases(long *gyro, long *accel, unsigned char hw_test)
        int get_st_biases(long *gyro, long *accel, unsigned char hw_test);
        //static int accel_self_test(long *bias_regular, long *bias_st)
        int accel_self_test(long *bias_regular, long *bias_st);
        //static int get_accel_prod_shift(float *st_shift)
        int get_accel_prod_shift(float *st_shift);
        //static int gyro_self_test(long *bias_regular, long *bias_st)
        int gyro_self_test(long *bias_regular, long *bias_st);
        //static inline unsigned short inv_row_2_scale(const signed char *row)
        unsigned short inv_row_2_scale(const signed char *row);
        //static inline unsigned short inv_orientation_matrix_to_scalar(const signed char *mtx)
        unsigned short inv_orientation_matrix_to_scalar(const signed char *mtx);
        //static void tap_cb(unsigned char direction, unsigned char count)
        static void tap_cb(unsigned char direction, unsigned char count);
        //static void android_orient_cb(unsigned char orientation)
        static void android_orient_cb(unsigned char orientation);
        //static int decode_gesture(unsigned char *gesture)
        int decode_gesture(unsigned char *gesture);
};

extern InertialSensor myMPU6050;

#endif	/* CONFIG_MPU6050_H */

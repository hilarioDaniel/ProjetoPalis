#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// Configurações de WiFi e UDP
WiFiUDP Udp;
static const float ACCEL_SENS = 4096.0; // Accel Sensitivity with +/- 8g scale
static const float GYRO_SENS  = 65.5;   // Gyro Sensitivity with +/- 500 deg/s scale
const int MPU = 0x68; // MPU6050 I2C address
IPAddress outIp(192, 168, 0, 108); // IP do computador para envio de dados
const unsigned int outPort = 1245; // Porta remota para envio de dados

// Configurações para leitura dos dados
int16_t ax, ay, az;
int16_t gx, gy, gz;
uint32_t timestamp;

// Definições de sensor e controle
MPU6050 mpu;

void setup(void)
{
    Serial.begin(115200);
    Serial.println("Inicializando...");

    // Conexão com Wi-Fi
    WiFi.begin("NTA-UFU", "ntaufu2023");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Conectando ao WiFi...");
    }
    Serial.println("Conectado ao WiFi!");

    // Inicialização do MPU6050
    Wire.begin();
    mpu.initialize();
    if (mpu.testConnection()) {
        Serial.println("Conexão com o MPU6050 bem-sucedida.");
    } else {
        Serial.println("Falha na conexão com o MPU6050.");
        while (1); // Se falhar, para a execução
    }

    // Calibração dos sensores
    Serial.flush();
    while (!Serial.available()) {
        Serial.println(F("Digite qualquer caractere para iniciar a calibração.\n"));
        delay(2000);
    }
    Serial.flush();

    mpu.CalibrateAccel(5);
    mpu.CalibrateGyro(5);
    mpu.PrintActiveOffsets();
    mpu.setZAccelOffset(mpu.getZAccelOffset() / 6);
}

void loop(void)
{
    // Ler dados de aceleração e giroscópio diretamente
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    // Capturar o timestamp 
    timestamp = millis(); // Timestamp em milissegundos

    // Imprimir valores para depuração
    Serial.print("Timestamp: ");
    Serial.println(timestamp);
    
    Serial.print("Aceleração: ");
    Serial.print((ax) / ACCEL_SENS); Serial.print(", ");
    Serial.print((ay) / ACCEL_SENS); Serial.print(", ");
    Serial.println((az) / ACCEL_SENS);

    Serial.print("Giroscópio: ");
    Serial.print((gx) / GYRO_SENS); Serial.print(", ");
    Serial.print((gy) / GYRO_SENS); Serial.print(", ");
    Serial.println((gz) / GYRO_SENS);

    // Enviar dados via UDP diretamente
    Udp.beginPacket(outIp, outPort);
    Udp.write((uint8_t*)&timestamp, sizeof(timestamp)); // Enviar o timestamp
    Udp.write((uint8_t*)&ax, sizeof(ax)); // Enviar ax
    Udp.write((uint8_t*)&ay, sizeof(ay)); // Enviar ay
    Udp.write((uint8_t*)&az, sizeof(az)); // Enviar az
    Udp.write((uint8_t*)&gx, sizeof(gx)); // Enviar gx
    Udp.write((uint8_t*)&gy, sizeof(gy)); // Enviar gy
    Udp.write((uint8_t*)&gz, sizeof(gz)); // Enviar gz
    Udp.endPacket();

    // Delay para evitar sobrecarga no envio de dados
    delay(2000);
}

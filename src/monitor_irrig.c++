#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Otimização 1: Definir constantes com tipos de dados menores e mais precisos
#define BUTTON_PIN_P     18    // uint8_t seria ideal, mas #define usa inteiros
#define LED_PIN_P        19    
#define BUTTON_PIN_K     5     
#define LED_PIN_K        17    
#define PIN_LDR_PH       34    
#define PIN_DHT          23    
#define PIN_RELE_IRR     4     //

// Otimização 2: Usar tipos de dados compactos
const uint8_t DHT_MODEL = DHT22;
const uint16_t SERIAL_BAUD = 115200;
const uint16_t INTERVAL_MS = 1000;  // Tempo entre leituras

// Otimização 3: Valores constantes como constexpr para otimização em tempo de compilação
constexpr float UMIDADE_IDEAL = 80.0f;  // Uso de float com precisão reduzida
constexpr int8_t PH_IDEAL = 6;
constexpr uint16_t IRRIGACAO_CURTA = 1500;
constexpr uint16_t IRRIGACAO_LONGA = 3000;

// Inicialização de componentes com referências diretas
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(PIN_DHT, DHT_MODEL);

// Otimização 4: Variáveis globais minimizadas e com tipos específicos
uint32_t ultimoTempo = 0;

void setup() {
  // Otimização 5: Configurações de pino mais compactas
  const uint8_t input_pins[] = {BUTTON_PIN_P, BUTTON_PIN_K};
  const uint8_t output_pins[] = {LED_PIN_P, LED_PIN_K, PIN_RELE_IRR};

  // Configuração de pinos em único loop
  for (uint8_t pin : input_pins) {
    pinMode(pin, INPUT_PULLUP);
  }
  
  for (uint8_t pin : output_pins) {
    pinMode(pin, OUTPUT);
  }

  // Otimização 6: Inicialização serial com verificação de erro
  Serial.begin(SERIAL_BAUD);
  while (!Serial); // Aguarda porta serial estar pronta

  // Inicialização de sensores
  dht.begin();
  lcd.init();
  lcd.backlight();

  // Cabeçalho otimizado para Serial Plotter
  Serial.println(F("Umidade,Temp,pH,N_P,N_K"));
}

void loop() {
  uint32_t tempoAtual = millis();
  
  // Otimização 7: Redução de chamadas de função e processamento
  if (tempoAtual - ultimoTempo >= INTERVAL_MS) {
    ultimoTempo = tempoAtual;

    // Otimização 8: Uso de variáveis locais de tipos menores
    bool nivel_P = digitalRead(BUTTON_PIN_P) == LOW;
    bool nivel_K = digitalRead(BUTTON_PIN_K) == LOW;

    // Otimização 9: Conversão de pH com menor overhead
    int8_t ldrScaled_PH = map(analogRead(PIN_LDR_PH), 0, 4095, 0, 14);

    // Leitura de sensor com tratamento de erro compacto
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // Otimização 10: Evitar múltiplas verificações
    if (!isnan(h) && !isnan(t)) {
      // Formato compacto para Serial Plotter
      Serial.print(h, 1);     // Umidade com 1 casa decimal
      Serial.print(',');
      Serial.print(t, 1);     // Temperatura com 1 casa decimal
      Serial.print(',');
      Serial.print(ldrScaled_PH);
      Serial.print(',');
      Serial.print(nivel_P);  
      Serial.print(',');
      Serial.println(nivel_K);

      // Controle de irrigação otimizado
      uint16_t time_irrig = ((!nivel_P || !nivel_K || 
                               ldrScaled_PH < PH_IDEAL || 
                               h < UMIDADE_IDEAL) ? 
                               IRRIGACAO_LONGA : 
                               IRRIGACAO_CURTA);

      // Acionamento de irrigação com menor overhead
      digitalWrite(PIN_RELE_IRR, HIGH);
      delay(time_irrig);
      digitalWrite(PIN_RELE_IRR, LOW);

      // Atualização LCD otimizada
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(F("P:")); 
      lcd.print(nivel_P ? F("OK") : F("LOW"));
      lcd.print(F(" K:")); 
      lcd.print(nivel_K ? F("OK") : F("LOW"));
      
      lcd.setCursor(0, 1);
      lcd.print(F("pH:")); 
      lcd.print(ldrScaled_PH);
      lcd.print(F(" Umi:")); 
      lcd.print(static_cast<int>(h));
      lcd.print('%');
    }
  }
}
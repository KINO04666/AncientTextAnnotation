-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document` (
  `user_id` bigint NOT NULL,
  `project_id` bigint NOT NULL,
  `doc_id` bigint NOT NULL AUTO_INCREMENT,
  `doc_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `doc_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `doc_describe` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `doc_create` datetime(6) DEFAULT NULL,
  `doc_modify` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`doc_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `project_id` (`project_id`) USING BTREE,
  CONSTRAINT `document_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `document_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
INSERT INTO `document` VALUES (1,1,6,'ggg','s','kjkjk','2024-12-12 17:44:06.000000','2024-12-12 17:49:57.000000'),(1,1,7,'123','','123','2024-12-16 17:59:52.000000','2024-12-16 17:59:52.000000'),(5,19,19,'关系定义-样例.xlsx','id,text,source,target,description,path,,,,\narrive,到达,person,location,表达某人到达某地的关系。,/,,,,\nbelong,属地,location,location,表示一个地点属于另一个更大的地理区域。,/,,,,\nattack,攻伐,person,location,描述一个人或集体对某个地点进行攻击或征服的行为。,/,,,,\nmanage,管理,person,position,一个人在某个职位上进行管理工作的情况。,/,,,,\nborn,生于（地点）,person,location,一个人出生在某个特定地点。,/,,,,\ndispatch,派遣,person,location,某人被派遣到另一个地点去执行任务。,/,,,,\nholdposition,任职 & 爵位 & 谥号,person,position,描述一个人担任某个职位、被授予爵位或谥号的情况。,/,,,,\nfather,父,person,person,表达亲子关系中的父亲与子女之间的联系。,/,,,,\nkill,杀,person,person,表示一个人杀害另一个人的行为。,/,,,,\nalias,别名,person,person,一个人或物体的其他名称或称呼。,/,,,,\nlocate,位于,location,location,表达一个地点在另一个地点内部或部分地区的关系。,/,,,,\ngrant,封 & 赐官,person,position,表示某个权力机构或个人授予某人官职或头衔。,/,,,,\nauthor,作者,person,book,表达一个人是某本书的作者的关系。,/,,,,\n,,,,,,,,,\n,,,,,,,,,\n,,,,,,,,,\n,,,,,,,,,\n,,,,,,,,,Ï\n','','2024-12-17 00:04:12.000000','2024-12-17 00:04:12.000000'),(5,19,22,'IoT-Lecture6.pdf','第 6 讲    物联网 RFID 技术 及应用        计科 22 级          1. RFID 概述   1 、自动识别技术 （   AIDC  ） ： 条码识别、磁卡识别、 IC  卡识别、射频识别、光学字符识别、生物识别、图像识别    •   比较：    中国自动识别技术协会 ： http://www.aimchina.org.cn   2 、 射频识别技术 （ Radio Frequency Identification ， RFID ）    •   通过无线射频方式进行非接触双向数据 传输 ， 以 达到识别目标和数据 交换的目的 ，属于 自动识别技术的一种    历史    •   1948 年 Stockman 的 论文 “利用反射功率的通讯”奠定了理论基础    •   1960 年代出现第一个商业应用系统 — 商品电子监视器    •   1990 年代组建 RFID 技术标准机构 — 全球产品电子编码协会 EPCglobal    •   2003 年沃尔玛宣布采用 RFID 技术追踪其供应链系统中商品        3 、 RFID 系统的构成    •   电子标签 （ Tag ）：附着在物体上标识目标对象，由耦合元件及芯片 组成，每个标签具有唯一的电子编码，不可修改    •   读写器 （ Reader ）   ：读取 ( 或写入 ) 标签信息的设备，配有天线    •   RFID 中间件 （   Middleware  ）：位于硬件和应用程序之间的通用服务， 具有标准的程序接口和协议    •   应用系统软件 ：针对不同行业特定需求开发的软件   4 、 RFID 的工作原理    •   标签进入磁场后，如果接收到读写器发出的特殊射频信号，就能凭借 感应电流所获得的能量发送出存储在芯片中的信息 (Passive   Tag ，无  源标签或被动标签 ) ，或者主动发送某一频率的信号 (Active   Tag ，有  源标签或主动标签 ) ，读写器读取信息并解码后，送至中央信息系统 进行有关数据处理。       5 、 RFID 系统的分类     6 、 RFID 的工作频率    •   工作频率不仅决定着射频识别系统工作原理（电感耦合还是电磁耦 合）、识别距离，还决定着电子标签及读写器实现的难易程度和设备  的成本    •   典型工作频率有：低频 125kHz 、 133kHz ，高频 6.75MHz 、 13.56MHz 、  27.125MHz ，超高频   433.92MHz 、 902MHz ～ 928MHz ，微波  2.45GHz 、 5.8GHz  等   7 、 RFID 的标准体系    •   RFID 技术标准组织：美国的 EPC Global 、国际标准化组织 ISO/IEC 、 日本的 Ubiquitous ID    •   相互之间不兼容，主要差别包括通讯方式、防冲突协议、数据格式等       •   EPC Global 制订了 EPC （ Electronic Product Code ）标准，使用 UHF  频段。    •   ISO 制定了 ISO14443A/B 、 ISO15693 与 ISO18000 标准，前两者采用  13.56MHz ，后者采用 860~930MHz    •   GB/T28925 - 2012 《 信息技术射频识别 2.45GHz 空中接口协议 》    •   GB/T 29768 - 2013 《 信息技术射频识别 800/900MHz 空中接口协议 》         8 、 ISO/IEC 14443 标准    •   规定了邻近卡（ PICC ）的物理特性；    •   需要供给能量的场的性质与特征，以及邻近耦合设备（ PCDs ）和邻  近卡（ PICCs ）之间的双向通信；    •   卡（ PICCs ）进入邻近耦合设备（ PCDs) 时的轮询，通信初始化阶段 的字符格式、帧结构、时序信息；    •   非接触的半双工的块传输协议，并定义了激活和停止协议的步骤；    •   传输协议同时适用于 TYPE A  和   TYPE B （主要的区别在于载波调制 深度及二进制数的编码方式和防冲突机制）      2. RFID 电子标签    •   电子标签，又名应答器，是一个微型无线收发装置，主要由芯片和内 置天线组成    •   本质上是一种数据载体，主要功能是携带物品信息，并提供接口，以 便读卡器能自动识别这些信息   1 、电子标签组成    •   天线：电标签和读写器沟通之桥。用来接收和发送信号。    •   电压调节器：将读写器送来的射频变成直流，并经过电容储存能量， 经过稳压电路提供电源。    •   调制器：调制逻辑电路 送 来数据，加载到天线。    •   解调器：解调取出载波信号。    •   逻辑控制单元：对读写器的送来信号进行译码，并按要求回送数据。    •   存储单元：系统运行和数据场所。   2 、 MIFARE  卡       •   Mifare 是恩智浦半导体公司（ NXP Semiconductors ）的注册商标    •   一系列依循 ISO/IEC 14443 - A 规格，利用射频识别（ 13.56MHz ）的多 种非接触式智能卡，包括 Mifare   S50 、 Mifare   S70 、 Mifare   UltraLight 、  Mifare   Pro 、   Mifare   Desfire 等    •   目前世界上使用量最大、技术最成熟、性能最稳定、内存容量最大，  业内有时把遵守 ISO14443A 标准的射频卡通称为“ Mifare ”    •   根据卡内芯片的不同，把 Mifare   UltraLight 称为 MF0 ， Mifare   S50 和  S70 称为 MF1 ， Mifare   Pro 称为 MF2 ， Mifare   Desfire 称为 MF3   3 、 Mifare   S50    （ 1 ） 主要指标    •   容量为 8K 位 EEPROM    •   分为 16 个扇区，每个扇区为 4 块，每块 16 个字节 ， 以块为存取单位    •   每个扇区有独立的一组密码及访问控制    •   每张卡有唯一序列号，为 32 位    •   具有防冲突机制，支持多卡操作    •   无电源，自带天线，内含加密控制逻辑和通讯逻辑电路    •   数据保存期为 10 年，可改写 10 万次，读无限次    •   工作温度： - 20 °C ~50 °C ( 湿度为 90%)    •   工作频率： 13.56MHZ    •   通信速率： 106 Kbps 读写距离： 10 cm 以内（与读写器有关）      （ 2 ）功能框图    •   S50 卡 由 1KB  的 EEPROM  、 RF  接口和数字式控制单元组成     （ 3 ）通信原理    复位应答 （ Answer to request ）    •   M1 射频卡的通讯协议和通讯波 特率是定义好的，当有卡片进 入读写器的操作范围时，读写 器以特定的协议与它通讯，从 而确定该卡是否为 M1 射频卡， 即验证卡片的卡型。      防冲突机制   ( Anticollision   Loop)    •   当有多张卡进入读写器操作范 围时，防冲突机制会从其中选  择一张进行操作，未选中的则  处于空闲模式等待下一次选卡， 该过程会返回被选卡的序列号   （ 3 ）通信原理    选择卡片 (Select Tag)    •   选择被选中的卡的序列号，并 同时返回卡的容量代码。      三次互相确认 ( 3 Pass Authentication )    •   选定要处理的卡片之后，读写  器就确定要访问的扇区号，并  对该扇区密码进行密码校验， 在三次相互认证之后就可以通 过加密流进行通讯。（在选择 另一扇区时，则必须进行另一  扇区密码校验。）      （ 4 ） 存储结构    •   M1 卡分为 16 个 扇区 Sector ，每个扇区由 4 块 Block   （块 0 、块 1 、块 2 、 块 3 ）组成， 64 个块 可 按绝对地址编号为 0~63      •   第 0 扇区的块 0 （即绝对地址 0 块），用于存放 厂商代码 UID ，已经固 化，不可更改。    •   每个扇区的块 0 、块 1 、块 2 为 数据块 ， 用作一般的数据保存，读 、 写  操作 ； 用作数据值，可初始化值、加值、减值、读值操作   •   每个扇区的块 3 为 控制块 ， 用于存放 密码 A 、存取控制、密码 B    •   每个扇区的 密码 和 存取控制 都是独立的，可以根据实际需要各自设定。 存取控制为 4 个字节，扇区中的每个块（包括数据块和控制块）的存  取条件是由密码和存取控制共同决定的   （ 5 ） 存 取控制    •   存取控制分 8 种情况，由控制块的第 6 ～ 9 字节决定    出厂时数据块控制位默认值 C1C2C3 = 000 ，控制块控制位默认值 C1C2C3   = 001 ，而 Byte9 一般是 69H ，所以出厂白卡的控制字通常是 FF078069H   •   数据块的存取控制                        •   keyA ：验证密码 A 可操作； keyB ：验证密码 B 可操作    •   key A|B ：验证密码 A 或 B 都可操作； never 验证哪个密码都不可操作      从表中可以看出，    •   C1C2C3=000( 出厂默认值 ) 时最宽松，验证密码 A 或密码 B 后可以进行 任何操作；    •   C1C2C3=111 无论验证哪个密码都不能进行任何操作，相当于把对应  的块冻结了；    •   C1C2C3=010 和 C1C2C3=101 都是只读，如果对应的数据块写入的是 一些可以给人看但不能改的基本信息，可以设为这两种模式；    •   C1C2C3=001 时只能读和减值，电子钱包一般设为这种模式，用户只 能查询或扣钱，不能加钱，充值的时候先改变控制位使卡片可以充值， 充完值再改回来      例如：当块 0 的存取控制位 C1 0   C2 0   C3 0 =1 0 0 时，验证密码 A 或密码 B 正  确后可读；验证密码 B 正确后可写；不能进行加值、减值操作。          •   控制块的存取控制                            从表中可以看出，    •   密码 A 是永远也读不出来的，如果用户的数据块指定了验证密码 A 却 忘了密码 A ，也就意味着这个数据块作废了，但本扇区其他数据块和  其他扇区的数据块不受影响；    •   存取控制总是可以读出来的，只要别忘了密码 A 或密码 B ；    •   存取控制的写控制在设置时一定要小心，一旦设成了“ Never” ，则整 个扇区的存取条件再也无法改变    •   C1C2C3=001( 出厂默认值 ) 时最宽松，除了密码 A 不能读之外，验证 了密码 A 其他读写操作都可以进行；      例如：当块 3 的存取控制位 C13 C23 C33=1 0 0 时，表示：    •   密码 A ：不可读，验证 KEYB 正确后，可写（更改）。    •   存取控制：验证 KEYA 或 KEYB 正确后，可读。    •   密码 B ：验证 KEYB 正确 后，可 写。      3. RFID 读写器    •   读写器又称阅读器，主要任务是向电子标签发射读取或者写入信号， 并接受 RFID 电子标签的应答，对电子标签的对象识别信息进行解码， 并将对象标识信息和其他信息传输到中央信息系统            分类    •   按工作方式分：全双工、半双工    •   按通信方式分：读写器先发言 RTF 、标签先发言 TTF    •   按工作频率分：低频 LF 、高频 HF 、超高频 UHF 、微波   1 、 RFID 的读写器的组成    •   通常由收发机、微处理器、存储器、报警器的输入 / 输出接口、通信接 口及电源等部件组成   2 、 MFRC522    •   NXP 针对“三表”应用推出的一款低电压、低成本、小尺寸的非接触 式读写卡芯片       （ 1 ） 主要指标    •   高集成度的调制解调电路    •   支持   ISO/IEC 14443 A/MIFARE  和   NTAG    •   读写器模式中操作距离高达 50mm    •   支持   ISO/IEC 14443 A 高达 848kbps  的传输速率    •   支持的主机接口：    － SPI  接口， 10Mbps     － I2C  接口，快速模式 400kbps ，高速模式 3400kbps    － RS232 UART 接口， 1228.8kbps    •   64B 收发 FIFO  缓冲区、 CRC 协处理器、可编程定时器 ...     （ 2 ）功能框图    •   模拟接口用来处理模拟信号的调制和解调    •   非接触式 UART 用来处理与主机通信时的协议要求    •   FIFO 缓冲区快速方便实现主机和非接触式 UART 间的数据传输     （ 3 ）模块参数         4. RFID 的 Arduino 库 — MFRC522    •   https://github.com/miguelbalboa/rfid                  •   当前版本 1.4.8 （ 20201230 ） 作者声明不再更新 功能    •   仅支持 SPI 接口，依赖库 SPI.h    •   支持 Arduino 多个型号，支持 ESP8266 （但部分示例不可用）    •   支持 ISO/IEC 14443 - 3 Type A ，不支持 Type B    •   仅支持 crypto1 - encrypted ，不要用于安全要求高的应用    •   支持 MIFARE Classic (1k, 4k, Mini) 及兼容卡，不支持 MIFARE  DESFire   （ 1 ） MFRC522 库的安装       （ 2 ） MFRC522 的部分 API              •   实例化                     •   PCD_Init ()  初始化 MFRC522 芯片    •   PCD_Reset ()  软重启 MFRC522  芯片并等待重启完毕    •   PCD_AntennaOn () 与 PCD_AntennaOff () 开启和关闭天线    •   PCD_GetAntennaGain () 获取当前 MFRC522 接收器的增益值    •   PCD_SetAntennaGain () 设置 MFRC522 接收器的增益值     •   Proximity Coupling Device (PCD)   is the actual RFID Reader  based on the NXP MFRC522 Contactless Reader Integrated Circuit.      •   Proximity Integrated Circuit Card (PICC)   is the RFID Card or Tag   using the ISO/IEC 14443A interface, e.g.  Mifare   or NTAG203.                            •   PCD_Authenticate ()   执行 MFRC522 的 MFAuthent 命令，开启加密认  证单元， PCD_StopCrypto1() 退出加密状态    •   其他为对数据块的读、写、加值、减值、存储、传输等操作   对数据块的操作      •   读   (Read) ：       读一个块；    •   写   ( Write ）：   写一个块；    •   加 （ Increment ）：   对数值块进行加值；    •   减 （ Decrement ）：     对数值块进行减值；    •   存储 （ Restore ）：   将块中的内容存到数据寄存器中；    •   传输 （ Transfer ）：   将数据寄存器中的内容写入块中；    •   中止 （ Halt ）：   将卡置于暂停工作状态；                   •   PCD_DumpVersionToSerial () 输出当前连接 PCD 的调试信息到串口    •   PICC_DumpToSerial () 输出已选择 PICC 的调试信息到串口    •   PICC_DumpDetailsToSerial () 输出选择 PICC 的卡信息 ( UID,SAK,Type )  到串口    •   PICC_DumpMifareClassicToSerial () 输出 MIFARE Classic PICC 的存 储信息到串口    •   PICC_DumpMifareClassicSectorToSerial () 输出某个扇区的存储信息                  •   PICC_IsNewCardPresent () Returns true if a PICC responds to  PICC_CMD_REQA. Only \"new\" cards in state IDLE are invited.  Sleeping cards in state HALT are ignored.       •   PICC_ReadCardSerial () ： Simple wrapper around  PICC_Select .  Returns true if a UID could be read. Remember to call  PICC_IsNewCardPresent (),  PICC_RequestA () or  PICC_WakeupA ()  first.       •   PICC_GetType () ： Translates the SAK (Select Acknowledge) to a  PICC type                      5. RFID 的 Arduino 库 — MFRC522 库的使用    【 例 1 】 与 NodeMCU 连接，串口输出读卡器和电子标签信息    •   示例 DumpInfo          •   显示结果     【 例 2 】 与 NodeMCU 连接，读写电子标签      •   打开示例 ReadAndWrite.ino         过程：    •   显示卡的 UID 和 PICC  类型    •   用密码 A 认证    •   显示第 1 扇区的全部数据    •   读取第 4 数据块全部数据    •   用密码 B 认证    •   修改第 4 数据块的数据    •   再次读取第 4 数据块全部数据    •   逐一比照读回数据是否为写入数据    •   再次显示第 1 扇区的全部数据               •   显示结果       【 例 3 】 与 NodeMCU 连接，读写电子标签      •   打开示例 labAccess.ino                 ','','2024-12-17 00:08:27.000000','2024-12-17 00:08:27.000000'),(5,19,24,'asd','','asd','2024-12-17 11:26:31.000000','2024-12-17 11:26:31.000000'),(5,19,25,'3.txt','// 引入必要的库文件\r\n#include <SPI.h>\r\n#include <MFRC522.h>\r\n#include <Wire.h>\r\n#include <Adafruit_GFX.h>\r\n#include <Adafruit_SSD1306.h>\r\n// #include <ESP8266WiFi.h>        // Wi-Fi功能库（如果需要拓展1）\r\n// #include <PubSubClient.h>       // MQTT库（如果需要拓展1）\r\n\r\n// 定义 RC522 模块引脚\r\n#define RST_PIN         D0    // RC522 的 RST 引脚连接到 NodeMCU 引脚 D0 (GPIO16)\r\n#define SS_PIN          D2    // RC522 的 SDA (SS) 引脚连接到 NodeMCU 引脚 D2 (GPIO4)\r\n\r\n// 定义 LED 引脚\r\n#define LED_PIN         D3    // LED 灯连接到 NodeMCU 引脚 D3 (GPIO0)\r\n\r\n// 定义 OLED 显示屏参数\r\n#define SCREEN_WIDTH    128   // OLED 显示屏宽度\r\n#define SCREEN_HEIGHT    64   // OLED 显示屏高度\r\n\r\n#define OLED_RESET      D0    // OLED 的 RESET 引脚，通过上拉电阻连接到 3.3V\r\n#define OLED_DC         D4    // OLED 的 DC 引脚连接到 NodeMCU 引脚 D4 (GPIO2)\r\n#define OLED_CS         D8    // OLED 的 CS 引脚连接到 NodeMCU 引脚 D8 (GPIO15)\r\nAdafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &SPI, OLED_DC, OLED_RESET, OLED_CS);\r\n\r\n// 创建 RC522 对象\r\nMFRC522 mfrc522(SS_PIN, RST_PIN);          // 创建 MFRC522 对象\r\n\r\n// Wi-Fi 和 MQTT 相关（如果需要拓展1，填写您的网络和服务器信息）\r\n/*\r\nWiFiClient espClient;\r\nPubSubClient client(espClient);\r\n\r\nconst char* ssid = \"your_SSID\";            // 替换为您的 Wi-Fi 名称\r\nconst char* password = \"your_PASSWORD\";    // 替换为您的 Wi-Fi 密码\r\nconst char* mqttServer = \"your_MQTT_server\"; // 替换为您的 MQTT 服务器地址\r\nconst int mqttPort = 1883;                 // MQTT 服务器端口\r\nconst char* mqttUser = \"your_MQTT_user\";   // MQTT 用户名（如果需要）\r\nconst char* mqttPassword = \"your_MQTT_password\"; // MQTT 密码（如果需要）\r\n*/\r\n\r\n// 全局变量\r\nint swipeCount = 0;  // 刷卡次数计数器\r\n\r\n// 设置自定义特征码（前三字节）\r\nconst byte featureCode[3] = {0xAA, 0xBB, 0xCC};\r\n\r\nvoid setup() {\r\n  // 初始化串口通讯\r\n  Serial.begin(115200);\r\n  while (!Serial); // 等待串口连接（用于调试）\r\n\r\n  // 初始化 SPI 总线\r\n  SPI.begin();\r\n\r\n  // 初始化 RC522 模块\r\n  mfrc522.PCD_Init();\r\n  Serial.println(\"RFID Reader initialized.\");\r\n\r\n  // 初始化 LED 引脚\r\n  pinMode(LED_PIN, OUTPUT);\r\n  digitalWrite(LED_PIN, LOW);\r\n\r\n  // 初始化 OLED 显示屏\r\n  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // 确认 I2C 地址\r\n    Serial.println(\"SSD1306 allocation failed\");\r\n    for(;;); // 停止程序\r\n  }\r\n  Serial.println(\"OLED initialized successfully.\");\r\n  display.clearDisplay();\r\n  display.setTextSize(1);\r\n  display.setTextColor(WHITE);\r\n  display.setCursor(0, 0);\r\n  display.println(\"Count:6,\\n Welcome \\nCard UID: da 7f 0a bf\");\r\n  display.display();\r\n\r\n  // 连接 Wi-Fi 和 MQTT 服务器（如果需要拓展1，取消注释）\r\n  /*\r\n  setupWiFi();\r\n  client.setServer(mqttServer, mqttPort);\r\n  */\r\n\r\n  // 如果需要写入特征码，取消以下注释，并在运行一次后再次注释\r\n  // writeFeatureCode();\r\n}\r\n\r\nvoid loop() {\r\n  // 处理 MQTT 连接（如果需要拓展1，取消注释）\r\n  /*\r\n  if (!client.connected()) {\r\n    reconnect();\r\n  }\r\n  client.loop();\r\n  */\r\n\r\n  // 检测是否有新卡片\r\n  if ( ! mfrc522.PICC_IsNewCardPresent()) {\r\n    return;\r\n  }\r\n  if ( ! mfrc522.PICC_ReadCardSerial()) {\r\n    return;\r\n  }\r\n\r\n  // 增加刷卡计数\r\n  swipeCount++;\r\n\r\n  // 读取卡片 UID\r\n  String uidStr = \"\";\r\n  for (byte i = 0; i < mfrc522.uid.size; i++) {\r\n    if(mfrc522.uid.uidByte[i] < 0x10) {\r\n      uidStr += \"0\";\r\n    }\r\n    uidStr += String(mfrc522.uid.uidByte[i], HEX);\r\n    uidStr += \" \";\r\n  }\r\n  uidStr.trim(); // 去除末尾空格\r\n  Serial.println(\"Card UID: \" + uidStr);\r\n\r\n  // 验证特征码\r\n  bool isAuthorized = checkAuthorization();\r\n\r\n  // 输出信息到串口监视器\r\n  Serial.print(\"Swipe Count: \");\r\n  Serial.println(swipeCount);\r\n\r\n  if (isAuthorized) {\r\n    Serial.println(\"Access Granted\");\r\n  } else {\r\n    Serial.println(\"Access Denied\");\r\n    // LED 闪烁 3 次\r\n    for(int i = 0; i < 3; i++) {\r\n      digitalWrite(LED_PIN, HIGH);\r\n      delay(200);\r\n      digitalWrite(LED_PIN, LOW);\r\n      delay(200);\r\n    }\r\n  }\r\n\r\n  // 在 OLED 上显示信息\r\n  display.clearDisplay();\r\n  display.setCursor(0, 0);\r\n  display.print(\"UID: \");\r\n  display.println(uidStr);\r\n  display.print(\"Count: \");\r\n  display.println(swipeCount);\r\n  \r\n  if (isAuthorized) {\r\n    display.println(\"Access Granted\");\r\n  } else {\r\n    display.println(\"Access Denied\");\r\n  }\r\n  display.display();\r\n\r\n  // 上传数据（如果需要拓展1，取消注释）\r\n  // uploadData(uidStr, isAuthorized);\r\n\r\n  // 停止读卡\r\n  mfrc522.PICC_HaltA();\r\n  mfrc522.PCD_StopCrypto1();\r\n}\r\n\r\n// 特征码验证函数\r\nbool checkAuthorization() {\r\n  // 选择目标扇区和块\r\n  byte sector         = 15;\r\n  byte blockAddr      = 60; // 扇区15的第2块，块地址为 (扇区号 * 4) + 块内偏移\r\n  MFRC522::StatusCode status;\r\n  byte buffer[18];\r\n  byte size = sizeof(buffer);\r\n\r\n  // 默认密钥\r\n  MFRC522::MIFARE_Key key;\r\n  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;\r\n\r\n  // 认证\r\n  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockAddr, &key, &(mfrc522.uid));\r\n  if (status != MFRC522::STATUS_OK) {\r\n    Serial.print(\"Authentication failed: \");\r\n    Serial.println(mfrc522.GetStatusCodeName(status));\r\n    return false;\r\n  }\r\n\r\n  // 读取数据\r\n  status = mfrc522.MIFARE_Read(blockAddr, buffer, &size);\r\n  if (status != MFRC522::STATUS_OK) {\r\n    Serial.print(\"Read failed: \");\r\n    Serial.println(mfrc522.GetStatusCodeName(status));\r\n    return false;\r\n  }\r\n\r\n  // 比较特征码\r\n  if (buffer[0] == featureCode[0] && buffer[1] == featureCode[1] && buffer[2] == featureCode[2]) {\r\n    Serial.println(\"Feature code matched.\");\r\n    return true;\r\n  } else {\r\n    Serial.println(\"Feature code did not match.\");\r\n    return false;\r\n  }\r\n}\r\n\r\n// 写入特征码函数（仅需执行一次）\r\nvoid writeFeatureCode() {\r\n  // 等待刷卡\r\n  Serial.println(\"Place your card to write feature code...\");\r\n  while ( ! mfrc522.PICC_IsNewCardPresent()) {\r\n    // 等待新卡片\r\n  }\r\n  if ( ! mfrc522.PICC_ReadCardSerial()) {\r\n    return;\r\n  }\r\n\r\n  // 选择目标扇区和块\r\n  byte sector         = 15;\r\n  byte blockAddr      = 60; // 扇区15的第2块，块地址为 (扇区号 * 4) + 块内偏移\r\n  MFRC522::StatusCode status;\r\n\r\n  // 默认密钥\r\n  MFRC522::MIFARE_Key key;\r\n  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;\r\n\r\n  // 数据块，前三字节为特征码，后续字节可自定义\r\n  byte dataBlock[16] = {featureCode[0], featureCode[1], featureCode[2], 0x01, 0x02, 0x03, 0x04, 0x05,\r\n                        0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D};\r\n\r\n  // 认证\r\n  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockAddr, &key, &(mfrc522.uid));\r\n  if (status != MFRC522::STATUS_OK) {\r\n    Serial.print(\"Authentication failed: \");\r\n    Serial.println(mfrc522.GetStatusCodeName(status));\r\n    return;\r\n  }\r\n\r\n  // 写入数据\r\n  status = mfrc522.MIFARE_Write(blockAddr, dataBlock, 16);\r\n  if (status != MFRC522::STATUS_OK) {\r\n    Serial.print(\"Write failed: \");\r\n    Serial.println(mfrc522.GetStatusCodeName(status));\r\n    return;\r\n  }\r\n  Serial.println(\"Feature code written successfully.\");\r\n\r\n  // 停止读卡\r\n  mfrc522.PICC_HaltA();\r\n  mfrc522.PCD_StopCrypto1();\r\n}\r\n\r\n// 以下是 Wi-Fi 和 MQTT 相关函数（如果需要拓展1，取消注释并填写相关信息）\r\n/*\r\nvoid setupWiFi() {\r\n  delay(10);\r\n  Serial.println();\r\n  Serial.print(\"Connecting to \");\r\n  Serial.println(ssid);\r\n\r\n  // 开始连接 Wi-Fi\r\n  WiFi.begin(ssid, password);\r\n\r\n  // 等待连接\r\n  while (WiFi.status() != WL_CONNECTED) {\r\n    delay(500);\r\n    Serial.print(\".\");\r\n  }\r\n\r\n  // 连接成功\r\n  Serial.println(\"\");\r\n  Serial.println(\"WiFi connected\");\r\n  Serial.println(\"IP address: \");\r\n  Serial.println(WiFi.localIP());\r\n}\r\n\r\nvoid uploadData(String uid, bool status) {\r\n  if (!client.connected()) {\r\n    reconnect();\r\n  }\r\n  client.loop();\r\n\r\n  String payload = \"{\";\r\n  payload += \"\\\"UID\\\":\\\"\" + uid + \"\\\",\";\r\n  payload += \"\\\"Status\\\":\\\"\" + String(status ? \"Success\" : \"Failed\") + \"\\\"\";\r\n  payload += \"}\";\r\n  Serial.println(\"Publishing message: \" + payload);\r\n\r\n  client.publish(\"rfid/access\", payload.c_str());\r\n}\r\n\r\nvoid reconnect() {\r\n  // 循环直到重新连接\r\n  while (!client.connected()) {\r\n    Serial.print(\"Attempting MQTT connection...\");\r\n    // 尝试连接\r\n    if (client.connect(\"NodeMCUClient\", mqttUser, mqttPassword)) {\r\n      Serial.println(\"connected\");\r\n    } else {\r\n      Serial.print(\"failed, rc=\");\r\n      Serial.print(client.state());\r\n      Serial.println(\" try again in 5 seconds\");\r\n      // 等待5秒后重试\r\n      delay(5000);\r\n    }\r\n  }\r\n}\r\n*/\r\n','','2024-12-17 11:29:10.000000','2024-12-17 11:29:10.000000'),(5,19,26,'123','','123','2024-12-17 14:21:30.000000','2024-12-17 14:21:30.000000'),(5,19,27,'IoT-Lecture6.pdf','第 6 讲    物联网 RFID 技术 及应用        计科 22 级          1. RFID 概述   1 、自动识别技术 （   AIDC  ） ： 条码识别、磁卡识别、 IC  卡识别、射频识别、光学字符识别、生物识别、图像识别    •   比较：    中国自动识别技术协会 ： http://www.aimchina.org.cn   2 、 射频识别技术 （ Radio Frequency Identification ， RFID ）    •   通过无线射频方式进行非接触双向数据 传输 ， 以 达到识别目标和数据 交换的目的 ，属于 自动识别技术的一种    历史    •   1948 年 Stockman 的 论文 “利用反射功率的通讯”奠定了理论基础    •   1960 年代出现第一个商业应用系统 — 商品电子监视器    •   1990 年代组建 RFID 技术标准机构 — 全球产品电子编码协会 EPCglobal    •   2003 年沃尔玛宣布采用 RFID 技术追踪其供应链系统中商品        3 、 RFID 系统的构成    •   电子标签 （ Tag ）：附着在物体上标识目标对象，由耦合元件及芯片 组成，每个标签具有唯一的电子编码，不可修改    •   读写器 （ Reader ）   ：读取 ( 或写入 ) 标签信息的设备，配有天线    •   RFID 中间件 （   Middleware  ）：位于硬件和应用程序之间的通用服务， 具有标准的程序接口和协议    •   应用系统软件 ：针对不同行业特定需求开发的软件   4 、 RFID 的工作原理    •   标签进入磁场后，如果接收到读写器发出的特殊射频信号，就能凭借 感应电流所获得的能量发送出存储在芯片中的信息 (Passive   Tag ，无  源标签或被动标签 ) ，或者主动发送某一频率的信号 (Active   Tag ，有  源标签或主动标签 ) ，读写器读取信息并解码后，送至中央信息系统 进行有关数据处理。       5 、 RFID 系统的分类     6 、 RFID 的工作频率    •   工作频率不仅决定着射频识别系统工作原理（电感耦合还是电磁耦 合）、识别距离，还决定着电子标签及读写器实现的难易程度和设备  的成本    •   典型工作频率有：低频 125kHz 、 133kHz ，高频 6.75MHz 、 13.56MHz 、  27.125MHz ，超高频   433.92MHz 、 902MHz ～ 928MHz ，微波  2.45GHz 、 5.8GHz  等   7 、 RFID 的标准体系    •   RFID 技术标准组织：美国的 EPC Global 、国际标准化组织 ISO/IEC 、 日本的 Ubiquitous ID    •   相互之间不兼容，主要差别包括通讯方式、防冲突协议、数据格式等       •   EPC Global 制订了 EPC （ Electronic Product Code ）标准，使用 UHF  频段。    •   ISO 制定了 ISO14443A/B 、 ISO15693 与 ISO18000 标准，前两者采用  13.56MHz ，后者采用 860~930MHz    •   GB/T28925 - 2012 《 信息技术射频识别 2.45GHz 空中接口协议 》    •   GB/T 29768 - 2013 《 信息技术射频识别 800/900MHz 空中接口协议 》         8 、 ISO/IEC 14443 标准    •   规定了邻近卡（ PICC ）的物理特性；    •   需要供给能量的场的性质与特征，以及邻近耦合设备（ PCDs ）和邻  近卡（ PICCs ）之间的双向通信；    •   卡（ PICCs ）进入邻近耦合设备（ PCDs) 时的轮询，通信初始化阶段 的字符格式、帧结构、时序信息；    •   非接触的半双工的块传输协议，并定义了激活和停止协议的步骤；    •   传输协议同时适用于 TYPE A  和   TYPE B （主要的区别在于载波调制 深度及二进制数的编码方式和防冲突机制）      2. RFID 电子标签    •   电子标签，又名应答器，是一个微型无线收发装置，主要由芯片和内 置天线组成    •   本质上是一种数据载体，主要功能是携带物品信息，并提供接口，以 便读卡器能自动识别这些信息   1 、电子标签组成    •   天线：电标签和读写器沟通之桥。用来接收和发送信号。    •   电压调节器：将读写器送来的射频变成直流，并经过电容储存能量， 经过稳压电路提供电源。    •   调制器：调制逻辑电路 送 来数据，加载到天线。    •   解调器：解调取出载波信号。    •   逻辑控制单元：对读写器的送来信号进行译码，并按要求回送数据。    •   存储单元：系统运行和数据场所。   2 、 MIFARE  卡       •   Mifare 是恩智浦半导体公司（ NXP Semiconductors ）的注册商标    •   一系列依循 ISO/IEC 14443 - A 规格，利用射频识别（ 13.56MHz ）的多 种非接触式智能卡，包括 Mifare   S50 、 Mifare   S70 、 Mifare   UltraLight 、  Mifare   Pro 、   Mifare   Desfire 等    •   目前世界上使用量最大、技术最成熟、性能最稳定、内存容量最大，  业内有时把遵守 ISO14443A 标准的射频卡通称为“ Mifare ”    •   根据卡内芯片的不同，把 Mifare   UltraLight 称为 MF0 ， Mifare   S50 和  S70 称为 MF1 ， Mifare   Pro 称为 MF2 ， Mifare   Desfire 称为 MF3   3 、 Mifare   S50    （ 1 ） 主要指标    •   容量为 8K 位 EEPROM    •   分为 16 个扇区，每个扇区为 4 块，每块 16 个字节 ， 以块为存取单位    •   每个扇区有独立的一组密码及访问控制    •   每张卡有唯一序列号，为 32 位    •   具有防冲突机制，支持多卡操作    •   无电源，自带天线，内含加密控制逻辑和通讯逻辑电路    •   数据保存期为 10 年，可改写 10 万次，读无限次    •   工作温度： - 20 °C ~50 °C ( 湿度为 90%)    •   工作频率： 13.56MHZ    •   通信速率： 106 Kbps 读写距离： 10 cm 以内（与读写器有关）      （ 2 ）功能框图    •   S50 卡 由 1KB  的 EEPROM  、 RF  接口和数字式控制单元组成     （ 3 ）通信原理    复位应答 （ Answer to request ）    •   M1 射频卡的通讯协议和通讯波 特率是定义好的，当有卡片进 入读写器的操作范围时，读写 器以特定的协议与它通讯，从 而确定该卡是否为 M1 射频卡， 即验证卡片的卡型。      防冲突机制   ( Anticollision   Loop)    •   当有多张卡进入读写器操作范 围时，防冲突机制会从其中选  择一张进行操作，未选中的则  处于空闲模式等待下一次选卡， 该过程会返回被选卡的序列号   （ 3 ）通信原理    选择卡片 (Select Tag)    •   选择被选中的卡的序列号，并 同时返回卡的容量代码。      三次互相确认 ( 3 Pass Authentication )    •   选定要处理的卡片之后，读写  器就确定要访问的扇区号，并  对该扇区密码进行密码校验， 在三次相互认证之后就可以通 过加密流进行通讯。（在选择 另一扇区时，则必须进行另一  扇区密码校验。）      （ 4 ） 存储结构    •   M1 卡分为 16 个 扇区 Sector ，每个扇区由 4 块 Block   （块 0 、块 1 、块 2 、 块 3 ）组成， 64 个块 可 按绝对地址编号为 0~63      •   第 0 扇区的块 0 （即绝对地址 0 块），用于存放 厂商代码 UID ，已经固 化，不可更改。    •   每个扇区的块 0 、块 1 、块 2 为 数据块 ， 用作一般的数据保存，读 、 写  操作 ； 用作数据值，可初始化值、加值、减值、读值操作   •   每个扇区的块 3 为 控制块 ， 用于存放 密码 A 、存取控制、密码 B    •   每个扇区的 密码 和 存取控制 都是独立的，可以根据实际需要各自设定。 存取控制为 4 个字节，扇区中的每个块（包括数据块和控制块）的存  取条件是由密码和存取控制共同决定的   （ 5 ） 存 取控制    •   存取控制分 8 种情况，由控制块的第 6 ～ 9 字节决定    出厂时数据块控制位默认值 C1C2C3 = 000 ，控制块控制位默认值 C1C2C3   = 001 ，而 Byte9 一般是 69H ，所以出厂白卡的控制字通常是 FF078069H   •   数据块的存取控制                        •   keyA ：验证密码 A 可操作； keyB ：验证密码 B 可操作    •   key A|B ：验证密码 A 或 B 都可操作； never 验证哪个密码都不可操作      从表中可以看出，    •   C1C2C3=000( 出厂默认值 ) 时最宽松，验证密码 A 或密码 B 后可以进行 任何操作；    •   C1C2C3=111 无论验证哪个密码都不能进行任何操作，相当于把对应  的块冻结了；    •   C1C2C3=010 和 C1C2C3=101 都是只读，如果对应的数据块写入的是 一些可以给人看但不能改的基本信息，可以设为这两种模式；    •   C1C2C3=001 时只能读和减值，电子钱包一般设为这种模式，用户只 能查询或扣钱，不能加钱，充值的时候先改变控制位使卡片可以充值， 充完值再改回来      例如：当块 0 的存取控制位 C1 0   C2 0   C3 0 =1 0 0 时，验证密码 A 或密码 B 正  确后可读；验证密码 B 正确后可写；不能进行加值、减值操作。          •   控制块的存取控制                            从表中可以看出，    •   密码 A 是永远也读不出来的，如果用户的数据块指定了验证密码 A 却 忘了密码 A ，也就意味着这个数据块作废了，但本扇区其他数据块和  其他扇区的数据块不受影响；    •   存取控制总是可以读出来的，只要别忘了密码 A 或密码 B ；    •   存取控制的写控制在设置时一定要小心，一旦设成了“ Never” ，则整 个扇区的存取条件再也无法改变    •   C1C2C3=001( 出厂默认值 ) 时最宽松，除了密码 A 不能读之外，验证 了密码 A 其他读写操作都可以进行；      例如：当块 3 的存取控制位 C13 C23 C33=1 0 0 时，表示：    •   密码 A ：不可读，验证 KEYB 正确后，可写（更改）。    •   存取控制：验证 KEYA 或 KEYB 正确后，可读。    •   密码 B ：验证 KEYB 正确 后，可 写。      3. RFID 读写器    •   读写器又称阅读器，主要任务是向电子标签发射读取或者写入信号， 并接受 RFID 电子标签的应答，对电子标签的对象识别信息进行解码， 并将对象标识信息和其他信息传输到中央信息系统            分类    •   按工作方式分：全双工、半双工    •   按通信方式分：读写器先发言 RTF 、标签先发言 TTF    •   按工作频率分：低频 LF 、高频 HF 、超高频 UHF 、微波   1 、 RFID 的读写器的组成    •   通常由收发机、微处理器、存储器、报警器的输入 / 输出接口、通信接 口及电源等部件组成   2 、 MFRC522    •   NXP 针对“三表”应用推出的一款低电压、低成本、小尺寸的非接触 式读写卡芯片       （ 1 ） 主要指标    •   高集成度的调制解调电路    •   支持   ISO/IEC 14443 A/MIFARE  和   NTAG    •   读写器模式中操作距离高达 50mm    •   支持   ISO/IEC 14443 A 高达 848kbps  的传输速率    •   支持的主机接口：    － SPI  接口， 10Mbps     － I2C  接口，快速模式 400kbps ，高速模式 3400kbps    － RS232 UART 接口， 1228.8kbps    •   64B 收发 FIFO  缓冲区、 CRC 协处理器、可编程定时器 ...     （ 2 ）功能框图    •   模拟接口用来处理模拟信号的调制和解调    •   非接触式 UART 用来处理与主机通信时的协议要求    •   FIFO 缓冲区快速方便实现主机和非接触式 UART 间的数据传输     （ 3 ）模块参数         4. RFID 的 Arduino 库 — MFRC522    •   https://github.com/miguelbalboa/rfid                  •   当前版本 1.4.8 （ 20201230 ） 作者声明不再更新 功能    •   仅支持 SPI 接口，依赖库 SPI.h    •   支持 Arduino 多个型号，支持 ESP8266 （但部分示例不可用）    •   支持 ISO/IEC 14443 - 3 Type A ，不支持 Type B    •   仅支持 crypto1 - encrypted ，不要用于安全要求高的应用    •   支持 MIFARE Classic (1k, 4k, Mini) 及兼容卡，不支持 MIFARE  DESFire   （ 1 ） MFRC522 库的安装       （ 2 ） MFRC522 的部分 API              •   实例化                     •   PCD_Init ()  初始化 MFRC522 芯片    •   PCD_Reset ()  软重启 MFRC522  芯片并等待重启完毕    •   PCD_AntennaOn () 与 PCD_AntennaOff () 开启和关闭天线    •   PCD_GetAntennaGain () 获取当前 MFRC522 接收器的增益值    •   PCD_SetAntennaGain () 设置 MFRC522 接收器的增益值     •   Proximity Coupling Device (PCD)   is the actual RFID Reader  based on the NXP MFRC522 Contactless Reader Integrated Circuit.      •   Proximity Integrated Circuit Card (PICC)   is the RFID Card or Tag   using the ISO/IEC 14443A interface, e.g.  Mifare   or NTAG203.                            •   PCD_Authenticate ()   执行 MFRC522 的 MFAuthent 命令，开启加密认  证单元， PCD_StopCrypto1() 退出加密状态    •   其他为对数据块的读、写、加值、减值、存储、传输等操作   对数据块的操作      •   读   (Read) ：       读一个块；    •   写   ( Write ）：   写一个块；    •   加 （ Increment ）：   对数值块进行加值；    •   减 （ Decrement ）：     对数值块进行减值；    •   存储 （ Restore ）：   将块中的内容存到数据寄存器中；    •   传输 （ Transfer ）：   将数据寄存器中的内容写入块中；    •   中止 （ Halt ）：   将卡置于暂停工作状态；                   •   PCD_DumpVersionToSerial () 输出当前连接 PCD 的调试信息到串口    •   PICC_DumpToSerial () 输出已选择 PICC 的调试信息到串口    •   PICC_DumpDetailsToSerial () 输出选择 PICC 的卡信息 ( UID,SAK,Type )  到串口    •   PICC_DumpMifareClassicToSerial () 输出 MIFARE Classic PICC 的存 储信息到串口    •   PICC_DumpMifareClassicSectorToSerial () 输出某个扇区的存储信息                  •   PICC_IsNewCardPresent () Returns true if a PICC responds to  PICC_CMD_REQA. Only \"new\" cards in state IDLE are invited.  Sleeping cards in state HALT are ignored.       •   PICC_ReadCardSerial () ： Simple wrapper around  PICC_Select .  Returns true if a UID could be read. Remember to call  PICC_IsNewCardPresent (),  PICC_RequestA () or  PICC_WakeupA ()  first.       •   PICC_GetType () ： Translates the SAK (Select Acknowledge) to a  PICC type                      5. RFID 的 Arduino 库 — MFRC522 库的使用    【 例 1 】 与 NodeMCU 连接，串口输出读卡器和电子标签信息    •   示例 DumpInfo          •   显示结果     【 例 2 】 与 NodeMCU 连接，读写电子标签      •   打开示例 ReadAndWrite.ino         过程：    •   显示卡的 UID 和 PICC  类型    •   用密码 A 认证    •   显示第 1 扇区的全部数据    •   读取第 4 数据块全部数据    •   用密码 B 认证    •   修改第 4 数据块的数据    •   再次读取第 4 数据块全部数据    •   逐一比照读回数据是否为写入数据    •   再次显示第 1 扇区的全部数据               •   显示结果       【 例 3 】 与 NodeMCU 连接，读写电子标签      •   打开示例 labAccess.ino                 ','','2024-12-17 14:21:35.000000','2024-12-17 14:21:35.000000'),(6,36,28,'李白 关山月.docx','《关山月》\n\n明月出天山，苍茫云海间。长风几万里，吹度玉门关。汉下白登道，胡窥青海湾。由来征战地，不见有人还。戍客望边邑，思归多苦颜。高楼当此夜，叹息未应闲。\n\n\n\n\n\n朗诵：\n\n以深沉而悠远的语调开始，“明月出天山，苍茫云海间”，想象着那轮明月从遥远的天山升起，照耀着苍茫的云海，营造出一种辽阔而神秘的氛围。接着，“长风几万里，吹度玉门关”，长风浩荡，穿越万里的距离，吹过了玉门关，将边疆的讯息带往中原。以下几句，诗人笔锋一转，开始描绘战争的残酷和戍边将士的思乡之情，“汉下白登道，胡窥青海湾。由来征战地，不见有人还。”最后，“戍客望边邑，思归多苦颜。高楼当此夜，叹息未应闲。”诗人以戍边将士的视角，表达了他们深深的思乡之情和无尽的叹息。\n\n\n\n分析：\n\n背景：这首诗是岑参在轮台（今新疆轮台县）送武判官归京时所作。诗中描绘了西北边疆壮丽瑰异的景色，表达了诗人对友人的惜别之情和因友人返京而产生的惆怅之情。\n\n内容：诗歌开篇即描写了北国的大雪，以“北风卷地白草折，胡天八月即飞雪”起笔，点出北国早雪的特点。接着用“忽如一夜春风来，千树万树梨花开”来描绘雪景，以春花喻冬雪，取喻新、设想奇，比喻中含有广阔而美丽的想象，同时字里行间又透露出蓬勃浓郁的无边春意。以下“散入珠帘湿罗幕”至“风掣红旗冻不翻”，则具体地描绘了雪中奇寒的景象，从各个不同角度表现了雪中的壮美和严寒，从而使这个送别场面显得空前阔大而情调哀伤。\n\n情感：诗人通过对西北边塞气候和壮丽景色的描写，表达了对友人的不舍和对边疆将士的敬仰。同时，诗歌也反映了诗人对边疆生活的热爱和对国家边疆安全的忧虑。\n\n\n\n意境和情感分析：\n\n一、意境分析\n\n苍茫辽阔的边塞图景：\n\n诗歌开篇以“明月出天山，苍茫云海间”描绘了边疆月夜的壮阔景象。天山、云海等自然元素交织在一起，营造出一种雄浑而神秘的氛围。\n\n“长风几万里，吹度玉门关”则进一步展现了边疆的辽阔与长风浩荡的气势，将读者的思绪引向遥远的边疆。\n\n战争与征战的残酷：\n\n“汉下白登道，胡窥青海湾”两句，通过历史典故的引用，展现了边疆地区战争频发、征战不断的残酷现实。\n\n“由来征战地，不见有人还”则直接点明了战争的残酷性，表达了诗人对战争所带来的伤亡和痛苦的深刻认识。\n\n戍边将士的思乡之情：\n\n诗歌的后半部分转向了对戍边将士思乡之情的描绘。“戍客望边邑，思归多苦颜”写出了将士们望着边疆的景象，思念家乡，脸上多现出愁苦的颜色。\n\n“高楼当此夜，叹息未应闲”则通过想象家中高楼上的妻子在月夜叹息，进一步强化了将士们的思乡之情和家人的思亲之苦。\n\n二、情感分析\n\n深沉的思乡之情：\n\n诗歌中弥漫着深沉的思乡之情。无论是戍边将士还是家中的妻子，都深深地思念着彼此，这种情感在诗歌中得到了充分的表达。\n\n对战争的反思与批判：\n\n诗人通过对边疆战争景象的描绘和对将士思乡之情的抒发，表达了对战争的反思与批判。他看到了战争所带来的痛苦和伤亡，对战争的残酷性有着深刻的认识。\n\n对和平的向往：\n\n在诗歌的结尾部分，诗人通过描绘将士们对家乡的思念和家人的叹息，表达了对和平生活的向往。他渴望战争结束，将士们能够回到家乡与亲人团聚。\n\n诗人的博大胸怀：\n\n整首诗歌不仅展现了边疆的壮丽景色和战争的残酷现实，更体现了诗人博大的胸怀和对民生的深切关怀。他关注着边疆将士的生死安危，同情着他们的思乡之苦，同时也对战争的残酷性进行了深刻的反思和批判。\n\n综上所述，《关山月》不仅是一幅描绘边疆壮丽景色和战争残酷现实的画卷，更是一首表达深沉思乡之情、对战争进行反思与批判、对和平生活充满向往的诗歌。它展现了李白作为唐代伟大诗人的卓越才华和深厚情感，同时也反映了唐代边疆社会的现实状况和人民的普遍心声。\n\n\n\n诗人生平与丝绸之路的关系\n\n李白（701~762年），字太白，号青莲居士，是唐代著名的浪漫主义诗人。他的诗歌作品以豪放、奔放、想象丰富而著称，被誉为“诗仙”。李白的家世与丝绸之路有着深厚的渊源。据记载，李白的先祖因故流亡到西域碎叶（今吉尔吉斯斯坦境内），隐姓埋名。到了李白父亲这一代，才重返内地，定居于西蜀绵州的昌隆（今四川江油）。因此，李白自幼就受到了西域文化的熏陶和影响。\n\n在李白的一生中，他多次游历边疆和丝绸之路沿线地区，亲身感受了边疆的壮丽景色和异域风情。这些经历不仅丰富了他的人生阅历和创作素材，也塑造了他豪放、奔放的诗歌风格。李白的诗歌作品中频频出现“胡姬酒肆”、“康国老胡”等富含丝路文化的意象，正是他对幼时生活挥之不去的记忆的多次释放。同时，李白也关注通过丝绸之路进入长安和中原的西域僧人、商人等，对他们的文化和生活方式进行了深入的描绘和赞美。\n\n综上所述，李白作为行走在丝绸之路上的唐代诗人代表，他的诗歌作品和生平经历都与丝绸之路紧密相关。他的诗歌作品不仅描绘了边疆的壮丽景色和战争的残酷，也表达了戍边将士的思乡之情和对丝绸之路的热爱。同时，他的生平经历也反映了丝绸之路对唐代文化和社会生活的深远影响。\n\n\n\n\n\n诵读经典：《关山月》李白_哔哩哔哩_bilibili\n\n\n\n','','2024-12-18 08:45:52.000000','2024-12-18 08:45:52.000000');
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enti_types`
--

DROP TABLE IF EXISTS `enti_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enti_types` (
  `enti_type_id` bigint NOT NULL AUTO_INCREMENT,
  `doc_id` bigint NOT NULL,
  `label` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` int DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT NULL,
  `color_background` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color_border` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color_fill` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`enti_type_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `enti_types_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `document` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enti_types`
--

LOCK TABLES `enti_types` WRITE;
/*!40000 ALTER TABLE `enti_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `enti_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entities`
--

DROP TABLE IF EXISTS `entities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entities` (
  `entity_id` bigint NOT NULL AUTO_INCREMENT,
  `doc_id` bigint NOT NULL,
  `original_id` int NOT NULL,
  `start_pos` int NOT NULL,
  `end_pos` int NOT NULL,
  `label` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color_background` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color_border` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color_fill` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`entity_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `entities_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `document` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entities`
--

LOCK TABLES `entities` WRITE;
/*!40000 ALTER TABLE `entities` DISABLE KEYS */;
INSERT INTO `entities` VALUES (1,26,1,0,2,'人物','李白','#FFCC80','#FF7043','#FF7043'),(2,26,2,13,14,'事件','歌声','#A5D6A7','#66BB6A','#66BB6A'),(3,26,3,4,5,'人物','杜甫','#FFCC80','#FF7043','#FF7043'),(4,26,4,8,10,'地点','长安','#90CAF9','#42A5F5','#42A5F5'),(5,26,5,20,22,'地点','山水','#A5D6A7','#66BB6A','#66BB6A'),(6,26,6,25,27,'主题','诗歌','#FFECB3','#FFD54F','#FFD54F'),(7,26,7,30,32,'情感','友谊','#FFAB91','#FF7043','#FF7043'),(8,26,8,35,37,'活动','旅途','#B39DDB','#7E57C2','#7E57C2');
/*!40000 ALTER TABLE `entities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `project_id` bigint NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `project_describe` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `project_create` datetime(6) DEFAULT NULL,
  `project_modify` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'abc','kjkjk','2024-12-12 17:08:42.000000','2024-12-12 17:15:44.000000',1),(14,'123',NULL,'2024-12-16 21:23:08.000000','2024-12-16 21:23:08.000000',1),(15,'123',NULL,'2024-12-16 21:24:54.000000','2024-12-16 21:24:54.000000',1),(16,'1234','123','2024-12-16 21:26:16.000000','2024-12-16 21:26:16.000000',1),(19,'123','123撒大苏打','2024-12-17 00:01:06.000000','2024-12-17 00:01:06.000000',5),(21,'13','13','2024-12-17 00:21:29.000000','2024-12-17 00:21:29.000000',5),(22,'13','13','2024-12-17 00:21:36.000000','2024-12-17 00:21:36.000000',5),(23,'123123123123123','123123123123123','2024-12-17 00:24:24.000000','2024-12-17 00:24:24.000000',5),(26,'123','1234','2024-12-17 00:28:25.000000','2024-12-17 00:28:25.000000',9),(27,'123','13','2024-12-17 00:29:09.000000','2024-12-17 00:29:09.000000',9),(28,'131313','131313131313131313131','2024-12-17 00:29:17.000000','2024-12-17 00:29:17.000000',9),(29,'123','123','2024-12-17 00:30:07.000000','2024-12-17 00:30:07.000000',9),(30,'123','123','2024-12-17 00:31:06.000000','2024-12-17 00:31:06.000000',9),(31,'13','1313','2024-12-17 00:31:11.000000','2024-12-17 00:31:11.000000',9),(32,'123','123','2024-12-17 00:32:12.000000','2024-12-17 00:32:12.000000',10),(33,'123','123','2024-12-17 00:33:28.000000','2024-12-17 00:33:28.000000',10),(34,'123123123','123123123123','2024-12-17 11:22:55.000000','2024-12-17 11:22:55.000000',5),(35,'asd','asdasd','2024-12-17 22:50:59.000000','2024-12-17 22:50:59.000000',5),(36,'123456','123456','2024-12-18 08:45:34.000000','2024-12-18 08:45:34.000000',6);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relations`
--

DROP TABLE IF EXISTS `relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relations` (
  `relation_id` bigint NOT NULL AUTO_INCREMENT,
  `doc_id` bigint NOT NULL,
  `from_entity_id` bigint NOT NULL,
  `to_entity_id` bigint NOT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`relation_id`),
  KEY `doc_id` (`doc_id`),
  KEY `from_entity_id` (`from_entity_id`),
  KEY `to_entity_id` (`to_entity_id`),
  CONSTRAINT `relations_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `document` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relations_ibfk_2` FOREIGN KEY (`from_entity_id`) REFERENCES `entities` (`entity_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relations_ibfk_3` FOREIGN KEY (`to_entity_id`) REFERENCES `entities` (`entity_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relations`
--

LOCK TABLES `relations` WRITE;
/*!40000 ALTER TABLE `relations` DISABLE KEYS */;
INSERT INTO `relations` VALUES (1,26,1,2,'创作','#FF7043'),(2,26,1,3,'朋友','#FFAB91'),(3,26,3,4,'居住地','#42A5F5'),(4,26,1,5,'喜好','#66BB6A'),(5,26,2,6,'主题','#FFD54F'),(6,26,5,8,'探索','#7E57C2'),(7,26,4,8,'旅途','#42A5F5'),(8,26,6,7,'情感','#FF7043');
/*!40000 ALTER TABLE `relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('123@qq.com','123456',1),('456@qq.com','123456',4),('820349335@qq.com','scrypt:32768:8:1$FPs5lobUB4NPtZQH$1dcc6853bf70d5ec30afe53d28aaaa52c1227668f36b5c6b338f2df928bda22a5a1f03009802f21c4643044f83432e647adb8ca01088ddd8e4ff81ac03ddcb49',5),('123456@qq.com','scrypt:32768:8:1$1jJ8GHKlhGs0ez35$16687d9b9c04461e6b0251f95176e052404f545b8cc86f58996238defa1e1caf6298c7d75ca6e367c656b7b13881f6fae03b467923e04d8d604a59483ecb4045',6),('faze@qq.com','scrypt:32768:8:1$tunYfuS4dMoxguLI$6b52bf9e9dcca0018fb105b30496922c05cdf8e422c6544789a9274c028d9a6fa65e1c5fb36596c9cbf0ebcdf437b07df101d161de5f364a0832d97dd38c65d6',7),('123123123@qq.com','scrypt:32768:8:1$cI0kqEbGe7YUGb3z$4d92a48f2642d744ec8d7d4d9c693aa4a53bdb99a758af98ae1a3401aca086e3959d640e5d843afbc2ede327933a5da84ff8e40f30eeeb0f7b5ccb556e222781',8),('13@q','scrypt:32768:8:1$FpQilreNlR0tqLHD$6764afa42412e8f4ffea9d1dfccb9552b5f228c1262fca03c525318a4812b4556b08fe8bef1d57c57077038364da33e5abfe7a278267e444a55ab9eba80f5e93',9),('131313@qqq','scrypt:32768:8:1$Emphy7K8aNceTzsY$29989e1a4e918bf165d03f515f1ee03e3471979e73559f1c970205b5e84260e806c4f5d7a5148102ec72d8095c4f1f6cb20855155dc8a2e8f0f818436687c9fc',10);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'test'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-18  8:46:38

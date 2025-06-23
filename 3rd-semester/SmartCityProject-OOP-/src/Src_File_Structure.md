Src_File_Structure: 

File Structure For My Project:

SmartCityProject/
│
├── models/           → All resource classes (CityResource, TransportUnit, etc.)
├── interfaces/       → Alertable, Reportable
├── zones/            → CityZone, ResourceHub, SmartGrid
├── repository/       → CityRepository<T>
├── utils/            → File handling (GSON), static metrics
├── gui/              → Swing-based GUI components
├── Main.java         → Entry point
└── gson/             → Include gson-2.8.9.jar or add via Maven


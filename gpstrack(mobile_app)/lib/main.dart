import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:location/location.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool _udpSendOn = false;
  String _gpsLocation = '';
  final Location _location = Location();
  late Timer _timer;
  String _ipAddress = '';
  int _portNumber = 0;
  late LocationData _locationData;
  String latitude = "";
  String longitude = "";
  static const githubUrl = 'https://github.com/AsaadDadoush';


  @override
  void initState() {
    super.initState();

    // Request location permission
    _location.requestPermission().then((permissionGranted) {
      if (permissionGranted == PermissionStatus.granted) {
        // Start tracking the location if permission is granted
        _location.onLocationChanged.listen((locationData) {
          // Update the GPS location field
          setState(() {
            _gpsLocation = '${locationData.latitude}, ${locationData.longitude}';
          });
        });
      }
    });
  }

  TextEditingController ipController = TextEditingController(text: '192.168.100.0');
  TextEditingController portController = TextEditingController(text: '5000');


  @override
  Widget build(BuildContext context)  {

    List<String> gpsValues = _gpsLocation.split(',');
    if (gpsValues.length > 1) {
      latitude = gpsValues[0];
      longitude = gpsValues[1];
      // rest of the code goes here
    }
    return MaterialApp(
      theme: ThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('GPS Tracker'),
        ),
        body: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Container(
                width: 300,
                height: 50,
                margin: const EdgeInsets.only(top: 30),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                    color: Colors.blue,
                    borderRadius: BorderRadius.circular(35)
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Latitude: $latitude',
                      style: const TextStyle(
                        fontSize: 20,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 300,
                height: 50,
                margin: const EdgeInsets.only(top: 10),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                    color: Colors.blue,
                    borderRadius: BorderRadius.circular(35)
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Longitude: $longitude',
                      style: const TextStyle(
                        fontSize: 20,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),

              Container(
                margin: const EdgeInsets.only(top: 15),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: Form(
                  child: Column(
                    children: [
                      TextFormField(
                        controller: ipController,
                        decoration: const InputDecoration(
                          labelText: 'IP Address',
                        ),
                        onChanged: (value) {
                          setState(() {
                            _ipAddress = value;
                          });
                        },
                        style: const TextStyle(
                          fontSize: 22,
                          color: Colors.blue,
                          fontFamily: 'Arial',
                        ),
                      ),
                      TextFormField(
                        controller: portController,
                        decoration: const InputDecoration(
                          labelText: 'Port Number',
                        ),
                        onChanged: (value) {
                          setState(() {
                            _portNumber = int.parse(value);
                          });
                        },
                        style: const TextStyle(
                          fontSize: 22,
                          color: Colors.blue,
                          fontFamily: 'Arial',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(top: 15),
                child: SingleChildScrollView(
                  child: InkWell(
                    child: RaisedButton.icon(
                      color: Colors.blue,
                      icon: _udpSendOn ? const Icon(Icons.pause) : const Icon(Icons.play_arrow),
                      label: Text(
                        _udpSendOn ? 'UDP Stream ON' : 'UDP Stream OFF',
                        style: const TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                        ),
                      ),
                      onPressed: () => _toggleUdpSend(),
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(35),
                      ),
                      elevation: 4,
                    ),
                    highlightColor: Colors.lightBlueAccent,
                    splashColor: Colors.lightBlue,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.only(top: 180),
                alignment: Alignment.bottomCenter,
                child: ButtonTheme(
                  minWidth: double.infinity,
                  child: Tooltip(
                    message: 'View on GitHub',
                    child: FlatButton.icon(
                      onPressed: () {
                        launch(githubUrl);
                      },
                      icon: const Icon(
                        Icons.link,
                        color: Colors.grey,
                      ),
                      label: const Text(
                        "View on GitHub",
                        style: TextStyle(
                          fontSize: 20,
                          fontFamily: 'Arial',
                          color: Colors.grey,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                      highlightColor: Colors.blue[100],
                    ),
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.only(top: 0, left: 20, right: 20, bottom: 20),
                alignment: Alignment.bottomCenter,
                child: const Text(
                  "This app was made for KAU Senior project",
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.lightBlueAccent,
                    fontSize: 12,
                  ),
                ),
              ),

            ],
          ),
        ),
      ),
    );
  }


  void _startTimer() {
    // Set the timer to run every 1 second
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      // Create a new RawDatagramSocket and bind it to a local port
      RawDatagramSocket.bind(InternetAddress.anyIPv4, 0).then((socket) {
        // Send the GPS data as a UDP stream to the desired address and port
        socket.send(utf8.encode(_gpsLocation), InternetAddress(_ipAddress), _portNumber);
      });
    });
  }

  void _stopTimer() {
    // Cancel the timer
    _timer.cancel();
  }

  void _toggleUdpSend() {
    setState(() {
      _udpSendOn = !_udpSendOn;
    });

    if (_udpSendOn) {
      _startTimer();
    } else {
      _stopTimer();
    }
  }
}
import 'package:flutter/material.dart';
import 'pages/create_wallet.dart';

void main() {
  runApp(MyCoinApp());
}

class MyCoinApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MyCoin Wallet',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: CreateWalletPage(),
    );
  }
}

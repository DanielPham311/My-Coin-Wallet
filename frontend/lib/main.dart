import 'package:flutter/material.dart';
import 'pages/create_wallet.dart';
import 'pages/dashboard.dart';

void main() => runApp(MyCoinApp());

class MyCoinApp extends StatelessWidget {
  const MyCoinApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MyCoin Wallet',
      theme: ThemeData(primarySwatch: Colors.indigo),
      initialRoute: '/',
      routes: {
        '/': (context) => CreateWalletPage(),
        // '/dashboard': (context) => DashboardPage(),
      },
    );
  }
}

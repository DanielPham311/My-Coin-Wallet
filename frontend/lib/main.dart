import 'package:flutter/material.dart';
import 'pages/create_wallet.dart';
import 'pages/dashboard.dart';
import 'pages/send_page.dart';

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
        '/dashboard': (context) => DashboardPage(),
        '/send': (context) {
          final args =
              ModalRoute.of(context)!.settings.arguments as Map<String, String>;
          return SendPage(
            address: args['address']!,
            privateKey: args['privateKey']!,
          );
        },
      },
    );
  }
}

import 'package:flutter/material.dart';
import 'package:frontend/pages/login.dart';
import 'package:frontend/pages/register.dart';
import 'package:frontend/pages/wallet_home.dart';
import 'pages/create_wallet.dart';
import 'pages/dashboard.dart';
import 'pages/send_page.dart';

void main() => runApp(const MyCoinApp());

class MyCoinApp extends StatelessWidget {
  const MyCoinApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MyCoin Wallet',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.indigo),
      initialRoute: '/login',
      routes: {
        '/': (context) => const CreateWalletPage(),
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/wallet': (context) => const WalletHome(),
        '/dashboard': (context) => DashboardPage(),
        '/send': (context) {
          final args = ModalRoute.of(context)!.settings.arguments
              as Map<String, String>;
          return SendPage(
            address: args['address']!,
            privateKey: args['privateKey']!,
          );
        },
      },
    );
  }
}

import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CreateWalletPage extends StatefulWidget {
  @override
  _CreateWalletPageState createState() => _CreateWalletPageState();
}

class _CreateWalletPageState extends State<CreateWalletPage> {
  String address = '';
  String privateKey = '';
  final api = ApiService();

  void createWallet() async {
    var wallet = await api.createWallet();
    setState(() {
      address = wallet['address'];
      privateKey = wallet['private_key'];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Create Wallet')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: createWallet,
              child: Text('Create Wallet'),
            ),
            SizedBox(height: 20),
            Text('Address: $address'),
            Text('Private Key: $privateKey'),
          ],
        ),
      ),
    );
  }
}

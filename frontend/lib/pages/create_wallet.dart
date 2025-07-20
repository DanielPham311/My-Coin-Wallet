import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CreateWalletPage extends StatefulWidget {
  const CreateWalletPage({super.key});

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
      appBar: AppBar(
        title: const Text('Create Wallet'),
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: Colors.black87,
          fontSize: 32,
          fontWeight: FontWeight.bold,
          fontFamily: 'RobotoMono',
          letterSpacing: 1.2,
          wordSpacing: 1.5,
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              'Create a new wallet to start using MyCoin.',
              style: TextStyle(
                fontSize: 16,
                color: Colors.black87,
                fontFamily: 'RobotoMono',
                letterSpacing: 1.2,
                wordSpacing: 1.5,
                height: 1.5,
                decoration: TextDecoration.none,
                decorationColor: Colors.transparent,
                decorationStyle: TextDecorationStyle.solid,
                decorationThickness: 1.0,
                fontWeight: FontWeight.w500,
                fontStyle: FontStyle.normal,
                backgroundColor: Colors.transparent,
              ),
            ),
            ElevatedButton(
              onPressed: createWallet,
              child: const Text('Create Wallet'),
            ),
            const SizedBox(height: 20),
            if (address.isNotEmpty) ...[
              const Text(
                'Your Wallet Address:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SelectableText(address, style: TextStyle(color: Colors.green)),
              const SizedBox(height: 10),
              const Text(
                'Your Private Key:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SelectableText(privateKey, style: TextStyle(color: Colors.red)),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  // navigate to next page
                  Navigator.pushNamed(
                    context,
                    '/dashboard',
                    arguments: {'address': address, 'privateKey': privateKey},
                  );
                },
                child: const Text('Continue to Dashboard'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

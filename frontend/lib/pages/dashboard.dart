import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/pages/history.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class DashboardPage extends StatefulWidget {
  @override
  _DashboardPageState createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  String address = '';
  String privateKey = '';
  int balance = 0;
  final api = ApiService();

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    address = args['address'];
    privateKey = args['privateKey'];
    fetchBalance();
  }

  void fetchBalance() async {
    final data = await api.getBalance(address);
    setState(() {
      balance = data['balance'];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 20),
            Text("Address:", style: TextStyle(fontWeight: FontWeight.bold)),
            SelectableText(address),
            const SizedBox(height: 20),
            Text("MyCoin Balance:", style: TextStyle(fontSize: 20)),
            Text(
              "$balance MYC",
              style: TextStyle(fontSize: 28, color: Colors.green),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: () async {
                final response = await http.get(
                  Uri.parse('http://localhost:5000/chain/validate'),
                );
                final result = jsonDecode(response.body);

                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text("Chain Validation"),
                    content: Text(result["message"]),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text("OK"),
                      ),
                    ],
                  ),
                );
              },
              child: const Text('Validate Blockchain'),
            ),

            ElevatedButton(
              onPressed: fetchBalance,
              child: const Text('Refresh Balance'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(
                  context,
                  '/send',
                  arguments: {'address': address, 'privateKey': privateKey},
                );
              },
              child: const Text('Send MyCoin'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        TransactionHistoryPage(address: address),
                  ),
                );
              },
              child: const Text('View Transaction History'),
            ),
          ],
        ),
      ),
    );
  }
}

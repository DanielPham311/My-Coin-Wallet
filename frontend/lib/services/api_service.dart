import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://10.0.2.2:5000";


  Future<Map<String, dynamic>> createWallet() async {
    final response = await http.post(Uri.parse('$baseUrl/wallet/create'));
    return json.decode(response.body);
  }

  Future<Map<String, dynamic>> getBalance(String address) async {
    final response = await http.get(Uri.parse('$baseUrl/wallet/$address'));
    return json.decode(response.body);
  }

  Future<void> sendTransaction(String sender, String receiver, int amount) async {
    await http.post(
      Uri.parse('$baseUrl/transaction'),
      headers: {"Content-Type": "application/json"},
      body: json.encode({"sender": sender, "receiver": receiver, "amount": amount}),
    );
  }

  Future<void> mineBlock() async {
    await http.get(Uri.parse('$baseUrl/mine'));
  }
}

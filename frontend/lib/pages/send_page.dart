import 'package:flutter/material.dart';
import '../services/api_service.dart';

class SendPage extends StatefulWidget {
  final String address;
  final String privateKey;

  SendPage({required this.address, required this.privateKey});

  @override
  _SendPageState createState() => _SendPageState();
}

class _SendPageState extends State<SendPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _recipientController = TextEditingController();
  final TextEditingController _amountController = TextEditingController();
  final ApiService api = ApiService();
  bool isLoading = false;

  void sendTransaction() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => isLoading = true);

    final response = await api.sendTransaction(
      sender: widget.address,
      recipient: _recipientController.text,
      amount: int.parse(_amountController.text),
      privateKey: widget.privateKey,
    );

    setState(() => isLoading = false);

    if (response.containsKey('error')) {
      _showDialog("Error", response['error']);
    } else {
      _showDialog("Success", "Transaction sent successfully!");
    }
  }

  void _showDialog(String title, String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('OK'))],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Send MyCoin")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _recipientController,
                decoration: InputDecoration(labelText: "Recipient Address"),
                validator: (value) =>
                    value!.isEmpty ? "Recipient address is required" : null,
              ),
              TextFormField(
                controller: _amountController,
                decoration: InputDecoration(labelText: "Amount"),
                keyboardType: TextInputType.number,
                validator: (value) =>
                    value!.isEmpty ? "Amount is required" : null,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: isLoading ? null : sendTransaction,
                child: isLoading ? CircularProgressIndicator() : Text("Send"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

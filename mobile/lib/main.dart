import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

const openapi = 'https://aziel-runtime.vibelock.workers.dev/openapi.json';
const mcp = 'https://aziel-runtime.vibelock.workers.dev/mcp';
const limitation =
    'AZBot is a skill, not a model, not a kernel, not a VPN. '
    'Jeeves is not sovereign. Paste the OpenAPI or MCP URL into ChatGPT, Grok, Venice, Claude, Cursor, or any other MCP/OpenAPI-capable assistant.';

void main() => runApp(const AzbotApp());

class AzbotApp extends StatelessWidget {
  const AzbotApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AZBot',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(primaryColor: const Color(0xFFC9A227)),
      home: const Home(),
    );
  }
}

class Home extends StatelessWidget {
  const Home({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AZBot')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(limitation),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => Clipboard.setData(const ClipboardData(text: openapi)),
            child: const Text('Copy OpenAPI'),
          ),
          const SizedBox(height: 8),
          FilledButton(
            onPressed: () => Clipboard.setData(const ClipboardData(text: mcp)),
            child: const Text('Copy MCP'),
          ),
        ],
      ),
    );
  }
}

import { Bot, Send, Sparkles } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const messages = [
  ["Officer", "Show robbery cases in Bengaluru South for the last 30 days."],
  ["CrimeX AI", "I found matching FIR records. Results are filtered by your role and jurisdiction."],
  ["Officer", "Summarize accused links across repeated vehicle numbers."],
];

export default function ChatbotPage() {
  return (
    <AppShell title="AI Chatbot" subtitle="Natural language access to authorized FIR intelligence.">
      <div className="grid gap-5 xl:grid-cols-[1fr_320px]">
        <Card className="min-h-[68vh]">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-blue-700 dark:text-blue-200" />
              Conversational Query
            </CardTitle>
          </CardHeader>
          <CardContent className="flex min-h-[58vh] flex-col justify-between gap-5">
            <div className="space-y-3">
              {messages.map(([sender, text]) => (
                <div key={text} className={sender === "CrimeX AI" ? "rounded-lg bg-blue-700 p-4 text-white" : "rounded-lg bg-white/70 p-4 dark:bg-slate-900/70"}>
                  <p className="mb-1 text-xs font-semibold opacity-80">{sender}</p>
                  <p className="text-sm leading-6">{text}</p>
                </div>
              ))}
            </div>
            <div className="flex gap-2">
              <Input placeholder="Ask about cases, accused, victims, hotspots, or reports" />
              <Button size="icon" aria-label="Send message">
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>AI Guardrails</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <Badge>
              <Sparkles className="mr-1 h-3 w-3" />
              Explainable
            </Badge>
            <p>Answers include authorized evidence references, role-based masking, and query trace metadata.</p>
            <p>Generated SQL is constrained to read-only approved official FIR tables.</p>
          </CardContent>
        </Card>
      </div>
    </AppShell>
  );
}


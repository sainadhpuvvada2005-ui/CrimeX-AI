"use client";

import { motion } from "framer-motion";
import { ArrowRight, Fingerprint, LockKeyhole, ShieldCheck } from "lucide-react";
import Link from "next/link";

import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen lg:grid-cols-[1.15fr_0.85fr]">
      <section className="relative flex min-h-[52vh] items-center overflow-hidden px-6 py-10 sm:px-10 lg:min-h-screen">
        <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(15,23,42,0.92),rgba(29,78,216,0.72)),url('https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=1800&q=80')] bg-cover bg-center" />
        <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-background/95 to-transparent" />
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative max-w-3xl text-white"
        >
          <div className="mb-6 inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/12 px-3 py-2 text-sm backdrop-blur-xl">
            <ShieldCheck className="h-4 w-4" />
            Karnataka Police secure intelligence workspace
          </div>
          <h1 className="text-4xl font-bold tracking-normal sm:text-5xl lg:text-6xl">CrimeX AI</h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-blue-50 sm:text-lg">
            Conversational crime intelligence, GIS awareness, network analysis, and operational reporting in a
            disciplined government-grade interface.
          </p>
        </motion.div>
      </section>

      <section className="flex items-center justify-center px-5 py-8 sm:px-8">
        <div className="w-full max-w-md">
          <div className="mb-5 flex justify-end">
            <ThemeToggle />
          </div>
          <Card>
            <CardContent className="p-6 sm:p-8">
              <div className="mb-6">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-700 text-white">
                  <Fingerprint className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold tracking-normal">Officer Login</h2>
                <p className="mt-2 text-sm text-muted-foreground">Access requires authorized role and session audit.</p>
              </div>
              <div className="space-y-4">
                <Input placeholder="Employee ID" />
                <Input placeholder="Password" type="password" />
                <Input placeholder="MFA Code" />
                <Button asChild className="w-full">
                  <Link href="/dashboard">
                    <LockKeyhole className="h-4 w-4" />
                    Sign in
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </main>
  );
}


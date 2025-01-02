import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "@/components/admin/ui/sonner";
import { secondaryFont } from "@/fonts";
import Header from "@/components/admin/Header";
import TanstackQueryProvider from "@/providers/TanstackQueryProvider";

export const metadata: Metadata = {
  title: "Web crapper",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={`h-screen flex flex-col overflow-y-auto ${secondaryFont.className}`}>
      <TanstackQueryProvider>

          <Header />
          <section className="flex-1 overflow-y-auto">
            <div className="container h-full">{children}</div>
          </section>
          <Toaster richColors closeButton />
        </TanstackQueryProvider>
      </body>
    </html>
  );
}

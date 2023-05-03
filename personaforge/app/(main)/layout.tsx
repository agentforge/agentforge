import "../styles/globals.css";
import "../styles/style.scss";
import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";
import { sfPro, inter } from "../fonts";
import Nav from "@/components/layout/nav";
import Footer from "@/components/layout/footer";
import { Suspense } from "react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={cx(sfPro.variable, inter.variable)}>
        <div className="fixed h-screen w-full bg-gradient-to-br from-white via-white to-indigo-100" />
        <Suspense fallback="...">
          {/* @ts-expect-error Server Component */}
          <Nav />
        </Suspense>
        {/* <main className="flex min-h-screen w-full flex-col items-center justify-center py-32"> */}
          {children}
        {/* </main> */}
        <Analytics />
        <Footer />
      </body>
    </html>
  );
}

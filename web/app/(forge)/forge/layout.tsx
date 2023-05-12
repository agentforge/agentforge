import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";
import { Suspense } from "react";
import { sfPro, inter } from "../../fonts";
import Nav from "@/components/layout/nav";
import "../../styles/globals.css";
import "../../styles/style.scss";

export const metadata = {
  title: 'AgentForge',
  description: 'Build, design, and evaluate agents.',
}

export default function ForgeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={cx(sfPro.variable, inter.variable)}>
        <div className="fixed h-screen w-full bg-gradient-to-br from-black via-black to-black" />
          {children}
          <Analytics />
      </body>
    </html>
  )
}

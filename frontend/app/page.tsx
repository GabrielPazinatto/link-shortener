"use client"

import { useState, useEffect } from "react"
import { HomeView } from "@/components/views/home-view"
import { LoginView } from "@/components/views/login-view"
import { RegisterView } from "@/components/views/register-view"
import { UserView } from "@/components/views/user-view"
import { ThemeToggle } from "@/components/theme-toggle"

type View = "home" | "login" | "register" | "user"

export default function URLShortener() {
  const [view, setView] = useState<View>("home")

  useEffect(() => {
    const userId = localStorage.getItem("id")
    if (userId && view === "home") {
      setView("user")
    }
  }, [])

  const handleNavigate = (newView: View) => {
    setView(newView)
  }

  return (
    <>
      <ThemeToggle />
      {view === "home" && <HomeView onNavigate={handleNavigate} />}
      {view === "login" && <LoginView onNavigate={handleNavigate} onLoginSuccess={() => setView("user")} />}
      {view === "register" && <RegisterView onNavigate={handleNavigate} />}
      {view === "user" && <UserView onNavigate={handleNavigate} onLogout={() => setView("home")} />}
    </>
  )
}

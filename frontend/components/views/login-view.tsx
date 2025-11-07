"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { parse } from "path"

const API_URL = process.env.NEXT_PUBLIC_API_URL || ""

interface LoginViewProps {
  onNavigate: (view: "register" | "user") => void
  onLoginSuccess: () => void
}

export function LoginView({ onNavigate, onLoginSuccess }: LoginViewProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()

    const body = new URLSearchParams();
    body.append('grant_type', 'password');
    body.append('username', username);
    body.append('password', password);

    try {
      const response = await fetch(`${API_URL}/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body,
      })

      const data = await response.json()

      if (response.ok && data.id !== null) {
        localStorage.setItem("accessToken", data.access_token)
        alert("Login Successful")
        setPassword("")
        onLoginSuccess()
      } else {
        alert("Login Failed: " + data.detail)
      }
    } catch (err) {
      console.error(err)
      alert("Login Failed")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Shortener</CardTitle>
          <CardDescription>A simple URL shortener</CardDescription>
          <CardTitle className="text-xl mt-4">Log In</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3 mb-6">
            <Button onClick={() => onNavigate("register")} variant="outline" className="flex-1">
              Register
            </Button>
            <Button onClick={() => onNavigate("user")} variant="outline" className="flex-1">
              User Page
            </Button>
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              Log In
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

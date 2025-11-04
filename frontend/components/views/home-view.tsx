"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface HomeViewProps {
  onNavigate: (view: "login" | "register" | "user") => void
}

export function HomeView({ onNavigate }: HomeViewProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Shortener</CardTitle>
          <CardDescription>A simple URL shortener</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <Button onClick={() => onNavigate("login")} className="w-full">
            Log In
          </Button>
          <Button onClick={() => onNavigate("register")} className="w-full">
            Register
          </Button>
          <Button onClick={() => onNavigate("user")} variant="outline" className="w-full">
            User Page
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox"

const API_URL = process.env.NEXT_PUBLIC_API_URL || ""
const REDIRECT_URL = process.env.NEXT_PUBLIC_REDIRECT_URL || ""

interface URLEntry {
  url: string
  short_url: string
}

interface UserViewProps {
  onNavigate: (view: "home" | "register") => void
  onLogout: () => void
}

export function UserView({ onNavigate, onLogout }: UserViewProps) {
  const [urlInput, setUrlInput] = useState("")
  const [urls, setUrls] = useState<URLEntry[]>([])
  const [selectedUrls, setSelectedUrls] = useState<Set<string>>(new Set())

  useEffect(() => {
    getUserData()
  }, [])

  const getUserData = async () => {
    try {
      const accessToken = localStorage.getItem("accessToken")
      if (!accessToken) {
        onNavigate("home")
        return
      }

      const response = await fetch(`${API_URL}/users/me/urls/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })

      if (!response.ok && response.status === 401) {
        alert("Session expired. Please log in again.")
        onLogout()
        return
      }

      if (!response.ok) {
        alert("Failed to get user data!")
        return
      }

      const jsonData = await response.json()

      setUrls(Array.isArray(jsonData) ? jsonData : [jsonData])
    } catch (err) {
      console.error(err)
      alert("Failed to get user data")
    }
  }

  const addNewUrl = async (e: React.FormEvent) => {
    e.preventDefault()

    const accessToken = localStorage.getItem("accessToken")

    if (!accessToken) return


    try {
      const response = await fetch(`${API_URL}/urls/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}`  },
        body: JSON.stringify({ url: urlInput }),
      })

      if (!response.ok) {
        alert("Failed to add new URL!")
        return
      }

      alert("URL added successfully!")
      setUrlInput("")
      getUserData()
    } catch (err) {
      console.error(err)
      alert("Failed to add new URL")
    }
  }

  const deleteSelected = async () => {
    const accessToken = localStorage.getItem("accessToken")
    if (!accessToken) return

    const urlsToDelete = Array.from(selectedUrls)

    try {
      const response = await fetch(`${API_URL}/urls/`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` },
        body: JSON.stringify(urlsToDelete),
      })

      if (!response.ok) {
        alert("Failed to delete selected URLs!")
      }

      setSelectedUrls(new Set())
      getUserData()
    } catch (err) {
      console.error(err)
      alert("Failed to delete selected URLs")
    }
  }

  const toggleUrlSelection = (shortUrl: string) => {
    const newSelected = new Set(selectedUrls)
    if (newSelected.has(shortUrl)) {
      newSelected.delete(shortUrl)
    } else {
      newSelected.add(shortUrl)
    }
    setSelectedUrls(newSelected)
  }

  const handleLogout = () => {
    localStorage.removeItem("id")
    localStorage.removeItem("username")
    setUrls([])
    setSelectedUrls(new Set())
    onLogout()
  }

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-3xl">Shortener</CardTitle>
            <CardDescription>A simple URL shortener</CardDescription>
            <CardTitle className="text-xl mt-4">User Page</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-3 mb-6">
              <Button onClick={handleLogout} variant="outline" className="flex-1 bg-transparent">
                Change Account
              </Button>
              <Button
                onClick={() => {
                  handleLogout()
                  onNavigate("register")
                }}
                variant="outline"
                className="flex-1"
              >
                New Account
              </Button>
            </div>

            <form onSubmit={addNewUrl} className="flex gap-2 mb-6">
              <Input
                type="text"
                placeholder="Enter url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                required
                className="flex-1"
              />
              <Button type="submit">Shorten</Button>
            </form>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label className="text-lg font-semibold">Shortened URLs</Label>
                <Button onClick={deleteSelected} variant="destructive" disabled={selectedUrls.size === 0}>
                  Delete Selected
                </Button>
              </div>

              <div className="border rounded-lg">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-12">#</TableHead>
                      <TableHead>URL</TableHead>
                      <TableHead>Shortened URL</TableHead>
                      <TableHead className="w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {urls.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center text-muted-foreground">
                          No URLs yet. Add one above!
                        </TableCell>
                      </TableRow>
                    ) : (
                      urls.map((entry, index) => (
                        <TableRow key={index}>
                          <TableCell>{index + 1}</TableCell>
                          <TableCell>
                            <a
                              href={entry.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline"
                            >
                              {entry.url}
                            </a>
                          </TableCell>
                          <TableCell>
                            <a
                              href={`${REDIRECT_URL}${entry.short_url}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline"
                            >
                              {REDIRECT_URL}
                              {entry.short_url}
                            </a>
                          </TableCell>
                          <TableCell>
                            <Checkbox
                              checked={selectedUrls.has(entry.short_url)}
                              onCheckedChange={() => toggleUrlSelection(entry.short_url)}
                            />
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

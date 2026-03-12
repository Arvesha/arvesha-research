'use client'

import { useCallback, useState } from 'react'
import useSWR from 'swr'
import { useDropzone } from 'react-dropzone'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { datasetsService } from '@/services/datasets'
import type { Dataset } from '@/types'
import toast from 'react-hot-toast'

export default function DatasetsPage() {
  const { data: datasets, isLoading, mutate } = useSWR<Dataset[]>('datasets', datasetsService.list)
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      setUploading(true)
      try {
        await datasetsService.upload(file, '')
        toast.success(`Uploaded ${file.name}`)
        mutate()
      } catch {
        toast.error(`Failed to upload ${file.name}`)
      } finally {
        setUploading(false)
      }
    }
  }, [mutate])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/plain': ['.txt'], 'application/json': ['.json'], 'text/csv': ['.csv'], 'application/pdf': ['.pdf'] },
  })

  const handleDelete = async (id: number) => {
    try {
      await datasetsService.delete(id)
      toast.success('Deleted')
      mutate()
    } catch {
      toast.error('Failed to delete')
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Datasets</h1>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
          }`}
        >
          <input {...getInputProps()} />
          {uploading ? (
            <div className="flex flex-col items-center gap-2"><Spinner /><p>Uploading...</p></div>
          ) : (
            <div>
              <div className="text-4xl mb-3">📁</div>
              <p className="text-lg font-medium">{isDragActive ? 'Drop files here' : 'Drag & drop files'}</p>
              <p className="text-sm text-muted-foreground mt-1">Supports JSON, CSV, TXT, PDF</p>
            </div>
          )}
        </div>

        {isLoading ? (
          <div className="flex justify-center py-8"><Spinner /></div>
        ) : (
          <div className="grid gap-4">
            {datasets?.map((ds) => (
              <Card key={ds.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <CardTitle className="text-base">{ds.name}</CardTitle>
                      <Badge variant="outline">{ds.file_type.toUpperCase()}</Badge>
                    </div>
                    <Button variant="destructive" size="sm" onClick={() => handleDelete(ds.id)}>Delete</Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-4 text-sm text-muted-foreground">
                    <span>📄 {ds.chunks_count} chunks</span>
                    <span>📅 {new Date(ds.created_at).toLocaleDateString()}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
            {datasets?.length === 0 && (
              <p className="text-center text-muted-foreground py-8">No datasets yet. Upload one above!</p>
            )}
          </div>
        )}
      </div>
    </MainLayout>
  )
}

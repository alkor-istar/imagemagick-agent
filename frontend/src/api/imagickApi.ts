export async function editImage(
    file: File,
    prompt: string
): Promise<Blob> {
    const formData = new FormData()
    formData.append("image", file)
    formData.append("prompt", prompt)

    const response = await fetch(
        `${import.meta.env.VITE_API_URL}/edit`,
        {
            method: "POST",
            body: formData,
        }
    )

    if (!response.ok) {
        throw new Error("Image edit failed")
    }

    return await response.blob()
}

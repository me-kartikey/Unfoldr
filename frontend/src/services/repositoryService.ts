import api from "@/api/axios";

export const uploadRepository = async (
    file: File
) => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/repositories/upload",
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data",
            },
        }
    );

    return response.data;
};
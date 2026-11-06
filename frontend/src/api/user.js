const API_URL = "http://localhost:8000"; // Revisa que sea el puerto de tu Django

export async function loginApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/token/`;
    const params = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };

    const response = await fetch(url, params);
    if (response.status !== 200) {
      throw new Error("Usuario o contraseña incorrecta");
    }
    const result = await response.json();
    return result;
  } catch (error) {
    throw new Error(error.message || "Error al iniciar sesión");
  }
}

export async function getMeApi(token) {
  try {
    const url = `${API_URL}/api/v1/auth/me/`;
    const params = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await fetch(url, params);
    const result = await response.json();
    return result;
  } catch (error) {
    throw error;
  }
}
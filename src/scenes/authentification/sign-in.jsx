import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../authentification/UserContext";
import { Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import {
  Box,
  Typography,
  useTheme,
  Button,
  TextField,
  Switch,
  Container,
  Paper,
  Snackbar,
  Alert
} from "@mui/material";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import logo from "../global/assets/logo.png";
import { tokens } from "../../theme";

const initialValues = {
  email: "",
  password: "",
};

const validationSchema = Yup.object().shape({
  email: Yup.string().email("Email invalide").required("L'email est requis"),
  password: Yup.string().required("Le mot de passe est requis"),
});

const SignIn = () => {
  const { login } = useContext(UserContext);
  const navigate = useNavigate();
  const [rememberMe, setRememberMe] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const handleSetRememberMe = () => setRememberMe(!rememberMe);

  const handleFormSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await fetch("http://localhost:5001/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.user.status !== "Activé") {
          setErrorMessage("Votre compte est désactivé. Contactez un administrateur.");
          setOpenSnackbar(true);
          return;
        }

        console.log("✅ Connexion réussie :", data);
        localStorage.setItem("token", data.token); // Stocker le token JWT
        login(data.user); // Met à jour le contexte utilisateur
        navigate("/dashboard");
      } else {
        setErrorMessage(data.message || "Échec de la connexion.");
        setOpenSnackbar(true);
      }
    } catch (error) {
      console.error("🚨 Erreur de connexion :", error);
      setErrorMessage("Une erreur s'est produite. Veuillez réessayer.");
      setOpenSnackbar(true);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box
      sx={{
        background: colors.primary[500],
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <Container maxWidth="xs">
        <Paper>
          {/* En-tête */}
          <Box
            sx={{
              background: theme.palette.info.main,
              borderRadius: "lg",
              mx: 2,
              mt: -3,
              p: 2,
              mb: 1,
              textAlign: "center",
            }}
          >
            <Typography variant="h4" fontWeight="medium" color="white">
              Connexion
            </Typography>
            <Box mt={1} />
            <a
              href="https://www.linkedin.com/company/queneysas/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <LinkedInIcon color="inherit" />
            </a>
          </Box>

          {/* Logo */}
          <img
            src={logo}
            alt="Logo"
            style={{
              maxWidth: "100px",
              display: "block",
              marginLeft: "auto",
              marginRight: "auto",
            }}
          />

          {/* Formulaire */}
          <Box pt={2} pb={2} px={2}>
            <Formik
              initialValues={initialValues}
              validationSchema={validationSchema}
              onSubmit={handleFormSubmit}
            >
              {({ isSubmitting }) => (
                <Form>
                  <Box
                    display="grid"
                    gap="30px"
                    gridTemplateColumns="repeat(4, minmax(0, 1fr))"
                    sx={{
                      "& > div": { gridColumn: "span 4" },
                    }}
                  >
                    <Field
                      as={TextField}
                      fullWidth
                      variant="filled"
                      type="email"
                      label="Email"
                      name="email"
                    />
                    <ErrorMessage
                      name="email"
                      component={Typography}
                      variant="body2"
                      color="error"
                    />

                    <Field
                      as={TextField}
                      fullWidth
                      variant="filled"
                      type="password"
                      label="Mot de passe"
                      name="password"
                    />
                    <ErrorMessage
                      name="password"
                      component={Typography}
                      variant="body2"
                      color="error"
                    />
                  </Box>

                  {/* Remember me */}
                  <Box display="flex" alignItems="center" ml={-1}>
                    <Switch
                      checked={rememberMe}
                      onChange={handleSetRememberMe}
                      sx={{
                        color: "white",
                        "&.Mui-checked": {
                          color: "white",
                          "& .MuiSwitch-thumb": {
                            backgroundColor: "white",
                          },
                        },
                      }}
                    />
                    <Typography
                      variant="button"
                      fontWeight="regular"
                      color="text"
                      onClick={handleSetRememberMe}
                      sx={{
                        cursor: "pointer",
                        userSelect: "none",
                        ml: -1,
                        color: "#ffffff",
                      }}
                    >
                      &nbsp;&nbsp;Se souvenir de moi
                    </Typography>
                  </Box>

                  {/* Bouton Connexion */}
                  <Box mt={4} mb={1}>
                    <Button
                      variant="contained"
                      fullWidth
                      type="submit"
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? "Connexion..." : "Se connecter"}
                    </Button>
                  </Box>

                  {/* Lien vers inscription */}
                  <Box mt={3} mb={1} textAlign="center">
                    <Typography variant="button" color="text">
                      Pas encore de compte ?{" "}
                      <Typography
                        component={Link}
                        to="/signup"
                        variant="button"
                        color={theme.palette.info.main}
                        fontWeight="medium"
                        sx={{
                          textGradient: `linear-gradient(to right, ${theme.palette.info.main}, ${theme.palette.primary.main})`,
                        }}
                      >
                        Inscrivez-vous
                      </Typography>
                    </Typography>
                  </Box>
                </Form>
              )}
            </Formik>
          </Box>
        </Paper>
      </Container>

      {/* Snackbar pour afficher les erreurs */}
      <Snackbar open={openSnackbar} autoHideDuration={5000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity="error" sx={{ width: "100%" }}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default SignIn;

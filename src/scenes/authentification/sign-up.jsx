import { Box, Button, TextField, useTheme } from "@mui/material";

import { useNavigate } from "react-router-dom";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";
import { tokens } from "../../theme";
import axios from "axios";
import { useState } from "react";

function SignUp() {
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [registrationStatus, setRegistrationStatus] = useState(null);

  const navigate = useNavigate();

  const handleFormSubmit = async (values) => {
    try {
      const response = await axios.post(
        "http://localhost:5001/api/signup",
        values
      );
      console.log(response.data); // Assuming the response contains the registration status
      setRegistrationStatus(response.data);
      console.log("done");
      // Update the registration status in the state
      navigate("/signin");
    } catch (error) {
      console.error("error from server");
      console.log(values);
    }
  };

  return (
    <Box m="20px">
      <Box textAlign={"center"} marginTop="150px">
        <Header title="S'INSCRIRE" subtitle="Créer un compte" />
      </Box>
      <Box
        sx={{
          background: colors.primary[500],
          display: "flex",
          justifyContent: "center",

          height: "100vh",
        }}
      >
        <Formik
          onSubmit={handleFormSubmit}
          initialValues={initialValues}
          validationSchema={checkoutSchema}
        >
          {({
            values,
            errors,
            touched,
            handleBlur,
            handleChange,
            handleSubmit,
          }) => (
            <form onSubmit={handleSubmit}>
              <Box
                display="grid"
                gap="30px"
                gridTemplateColumns="repeat(4, minmax(0, 1fr))"
                sx={{
                  "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
                }}
              >
                <TextField
                  fullWidth
                  variant="filled"
                  type="text"
                  label="first_name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.first_name}
                  name="first_name"
                  error={!!touched.first_name && !!errors.first_name}
                  helperText={touched.first_name && errors.first_name}
                  sx={{ gridColumn: "span 2" }}
                />
                <TextField
                  fullWidth
                  variant="filled"
                  type="text"
                  label="last_name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.last_name}
                  name="last_name"
                  error={!!touched.last_name && !!errors.last_name}
                  helperText={touched.last_name && errors.last_name}
                  sx={{ gridColumn: "span 2" }}
                />
                <TextField
                  fullWidth
                  variant="filled"
                  type="text"
                  label="Email"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.email}
                  name="email"
                  error={!!touched.email && !!errors.email}
                  helperText={touched.email && errors.email}
                  sx={{ gridColumn: "span 4" }}
                />
                <TextField
                  fullWidth
                  variant="filled"
                  type="text"
                  label="phone_number"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.phone_number}
                  name="phone_number"
                  error={!!touched.phone_number && !!errors.phone_number}
                  helperText={touched.phone_number && errors.phone_number}
                  sx={{ gridColumn: "span 4" }}
                />
                <TextField
                  fullWidth
                  variant="filled"
                  type="password" // Change the input type to "password"
                  label="Password" // Change the label to "Password"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.password} // Use the "password" value instead of "address1"
                  name="password" // Use the "password" name instead of "address1"
                  error={!!touched.password && !!errors.password} // Check for errors in the "password" field
                  helperText={touched.password && errors.password} // Display the helper text for "password" errors
                  sx={{ gridColumn: "span 4" }}
                />
              </Box>
              <Box display="flex" justifyContent="end" mt="20px">
                <Button type="submit" color="secondary" variant="contained">
                  S'inscrire
                </Button>
              </Box>
            </form>
          )}
        </Formik>
      </Box>
    </Box>
  );
}

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const checkoutSchema = yup.object().shape({
  first_name: yup.string().required("required"),
  last_name: yup.string().required("required"),
  email: yup.string().email("invalid email").required("required"),
  phone_number: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid")
    .required("required"),
  password: yup.string().required("required"), // Add the "password" field validation rule
});

const initialValues = {
  first_name: "",
  last_name: "",
  email: "",
  phone_number: "",
  password: "",
};

export default SignUp;

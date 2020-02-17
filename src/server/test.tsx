import React, { useState } from "react";
import "./styles.css";
import CustomDatePicker from "./custom-datepicker";
import CustomSelect from "./custom-select";
import { Form as FormikForm, Formik } from "formik";
import { Button } from "semantic-ui-react";
import { format } from "date-fns";
var xx = [{ value: 1, label: "init" }, { value: 2, label: "init" }];
const initialState: any = {
  datex: new Date(),
  driveTimes: xx[0].value
};

export default function App() {
  const [formValues, updateFormValues] = useState<any>(initialState);
  const [testOptions, setTestOptions] = useState([
    { value: 1, label: "test" },
    { value: 2, label: "teggg" }
  ]);

  function handleDatePickerBlur (
    setFieldValue: (fieldName: keyof any, value: any) => void
  ) {
    var opt = [{ value: 3, label: "new" }, { value: 4, label: "new new" }];
    var x = format(formValues.datex, "MM/dd/yyyy");
    // if (x === "02/10/2020") {
    console.log(format(formValues.datex, "MM/dd/yyyy"));
    setFieldValue("driveTimes", opt[1].value);
    setTestOptions(opt);
    // }
  }

  return (
    <Formik
      initialValues={{ ...formValues }}
      onSubmit={"" as any}
      render={({ values, setFieldValue }: any) => {
        // Initialize the form values into local state
        updateFormValues(values);

        return (
          <>
            <FormikForm className="ui form">
              <CustomDatePicker
                id="datex"
                name="datex"
                label=""
                placeholder="Choose date"
                //This one works fine on Desktop
                onBlur={() => {}}
                //This one works also on Mobile,
                //but late one step, check console
                onChange={() => handleDatePickerBlur(setFieldValue)}
              />
              <br />
              <br />
              <CustomSelect
                id="driveTimes"
                name="driveTimes"
                options={testOptions}
                label="Result"
                placeholder="Choose option"
              />
            </FormikForm>
            <br />
            <Button primary onClick={() => window.location.reload()}>
              Reload
            </Button>
          </>
        );
      }}
    />
  );
}

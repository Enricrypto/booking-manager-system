import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import BigContainer from "../../components/bigContainer/index.jsx";
import Input from "../input/index.jsx";
import InputField from "../inputField/index.jsx";
import styles from "./workerForm.module.css";
import Button from "../button/index.jsx";
import { createWorker } from "../../service/workers.js";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { workerSchema } from "../../validations/workerValidation.js";
import { toast } from "react-toastify";

const initialState = {
  username: "",
  firstname: "",
  lastname: "",
  email: "",
  password: "",
};

const WorkerForm = ({ textBtn }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(workerSchema),
  });

  const [newWorker, setNewWorker] = useState(initialState);

  const navigate = useNavigate();

  const { companyID } = useParams();

  const handleChange = ({ target }) => {
    setNewWorker({ ...newWorker, [target.name]: target.value });
  };

  const onSubmit = async () => {
    const resMsg = await createWorker(companyID, newWorker);
    if (resMsg?.error) {
      toast.error(resMsg?.msg);
    } else {
      toast.success(resMsg?.msg);
      navigate(`/admin-dashboard/${companyID}`);
    }
  };

  return (
    <main className={styles._mainContainer}>
      <BigContainer>
        <h1>Create Worker</h1>
        <form
          className={styles._form}
          onChange={handleChange}
          onSubmit={handleSubmit(onSubmit)}
        >
          <Input
            icon={<i className="fa-solid fa-circle-user"></i>}
            type="text"
            placeholder="Username"
            name="username"
            value={newWorker.username}
            register={register}
          />
          {errors?.username && (
            <small className={styles._fail}>
              <i className="fa-solid fa-circle-exclamation"></i>{" "}
              {errors.username?.message}
            </small>
          )}
          <Input
            icon={<i className="fa-solid fa-circle-user"></i>}
            type="text"
            placeholder="Firstname"
            name="firstname"
            value={newWorker.firstname}
            register={register}
          />
          {errors?.firstname && (
            <small className={styles._fail}>
              <i className="fa-solid fa-circle-exclamation"></i>{" "}
              {errors.firstname?.message}
            </small>
          )}
          <Input
            icon={<i className="fa-solid fa-circle-user"></i>}
            type="text"
            placeholder="Lastname"
            name="lastname"
            value={newWorker.lastname}
            register={register}
          />
          {errors?.lastname && (
            <small className={styles._fail}>
              <i className="fa-solid fa-circle-exclamation"></i>{" "}
              {errors.lastname?.message}
            </small>
          )}
          <Input
            icon={<i className="fa-solid fa-envelope"></i>}
            type="email"
            placeholder="email"
            name="email"
            value={newWorker.email}
            register={register}
          />
          {errors?.email && (
            <small className={styles._fail}>
              <i className="fa-solid fa-circle-exclamation"></i>{" "}
              {errors.email?.message}
            </small>
          )}
          <InputField
            icon="fa-solid fa-lock"
            type="password"
            placeholder="Password"
            name="password"
            register={register}
            errors={errors}
          />
          <Button type="submit" title={textBtn} />
        </form>
      </BigContainer>
    </main>
  );
};

export default WorkerForm;

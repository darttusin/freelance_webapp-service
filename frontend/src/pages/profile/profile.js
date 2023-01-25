import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "react-query";
import { Layout } from "../../components/Layout/Layot";
import avatar from "../../img/avatar.png";
import dots from "../../icons/dots.svg";
import avatar_hover from "../../img/avatar_hover.png";
import preview from "../../img/preview.jpg";
import { PortfolioCard } from "../../components/Сards/PortfolioCard/PortfolioCard";
import { FeedbackCard } from "../../components/Сards/FeedbackCard/FeedbackCard";
import { CustomSlider } from "../../components/Slider/CustomSlider";
import { CustomSelect } from "../../components/Select/Select";
import { DropDown } from "../../components/DropDown/DropDown";
import { DropDownItem } from "../../components/DropDown/DropDown";
import { Button } from "../../components/Button/Button";
import { changeProfile, getMyProfile } from "../../http/user";
import { roles } from "../../сonstants/constants";
import { setCookie } from "../../utils/cookie";
import { StarRating } from "../../components/StarRating/StarRating";
import "../../styles/profile.css";

export const Profile = ({ setToken }) => {
  const [user, setUser] = useState();

  const { data, isLoading, error } = useQuery("user", getMyProfile, {
    onSuccess: setUser,
  });

  const [role, setRole] = useState("influencer");
  const [isEditing, setIsEditing] = useState(false);
  const [isDropDown, setIsDropDown] = useState(false);
  const [isPortfolioOpend, setIsPortfolioOpend] = useState(false);
  const [mode, setMode] = useState(localStorage.getItem("mode"));
  const navigate = useNavigate();

  const onSelectChange = (e) => {
    setRole(e.label);
  };

  const onModeChange = (mode) => {
    setMode(mode);
    localStorage.setItem("mode", mode);
  };

  const editProfile = async () => {
    const response = await changeProfile({
      img_url: "string",
      description: "string",
      user_name: user.user_name,
    });

    setIsEditing(false);
  };

  const logout = () => {
    setToken("");
    setCookie("access_token", "");
    localStorage.setItem("id", "");
  };

  useEffect(() => {
    const id = localStorage.getItem("id");

    if (user) {
      if (user.user_id != id) {
        localStorage.setItem("id", user.user_id);
      }
    }
  }, [user]);

  if (isLoading) {
    return "Loading....";
  }

  if (user) {
    return (
      <Layout withFooter={true}>
        <div className="profile">
          {!isEditing && (
            <div className="profile__settings">
              <p className="profile-mode__title">Mode</p>
              <div
                onClick={() =>
                  onModeChange(mode === "performer" ? "customer" : "performer")
                }
                className={`profile-mods ${
                  mode == "performer" && "profile-mods_switch"
                }`}>
                <p
                  className={`profile__mode ${
                    mode == "customer" && "profile__mode_active"
                  }`}>
                  Заказчик{" "}
                </p>

                <p
                  className={`profile__mode ${
                    mode == "performer" && "profile__mode_active"
                  }`}>
                  Исполнитель
                </p>
              </div>

              <img
                alt=""
                onClick={() => {
                  setIsDropDown(true);
                }}
                src={dots}
              />
            </div>
          )}

          {isDropDown && (
            <DropDown>
              <DropDownItem onClick={() => setIsDropDown(false)}>
                отменить
              </DropDownItem>
              <DropDownItem
                onClick={() => {
                  setIsEditing(true);
                  setIsDropDown(false);
                }}>
                Редактировать
              </DropDownItem>
              <DropDownItem onClick={logout}>выйти с аккаунта</DropDownItem>
            </DropDown>
          )}
          <div className="profile__avatar">
            <img
              className=""
              alt=""
              src={avatar}
            />
            {isEditing && (
              <img
                className="profile_avatar_hover"
                src={avatar_hover}
                alt=""></img>
            )}
          </div>
          <div className="profile-description">
            {isEditing ? (
              <>
                <p className="profile__label">Имя</p>
                <input
                  className="profile__input"
                  name="user_name"
                  value={user.user_name}
                  onChange={(e) =>
                    setUser((prev) => ({
                      ...prev,
                      [e.target.name]: e.target.value,
                    }))
                  }
                />
              </>
            ) : (
              <p className="profile__name">{user.user_name}</p>
            )}
            {isEditing ? (
              <div>
                <p className="profile__label">Role:</p>
                <CustomSelect
                  className="profile__select"
                  onChange={onSelectChange}
                  options={roles}
                />
              </div>
            ) : (
              <p className="profile__role">Role: {role}</p>
            )}
            {isEditing ? (
              <Button
                text={"сохранить"}
                style={"white"}
                onClick={editProfile}>
                Сохранить
              </Button>
            ) : (
              <StarRating
                rating={5}
                readonly={true}
              />
            )}
          </div>
          <div className="profile-documents">
            <p className="profile__title">Личные документы</p>
          </div>

          <div className="profile-portfolio">
            <div className="profile__title profile-portfolio__title">
              <p>Портфолио</p>
              <img
                src={dots}
                alt=""
                onClick={() => setIsPortfolioOpend(true)}
                className="dots"></img>
            </div>

            {isPortfolioOpend ? (
              <DropDown>
                <DropDownItem onClick={() => setIsPortfolioOpend(false)}>
                  отменить
                </DropDownItem>
                <DropDownItem
                  onClick={() => {
                    navigate("./create-portfolio");
                  }}>
                  добавить новый элемент
                </DropDownItem>
              </DropDown>
            ) : (
              <CustomSlider>
                {user.user_portfolios.map((item, index) => (
                  <PortfolioCard
                    key={index}
                    title={item.portfolio_title}
                    description={item.portfolio_description}
                    preview={preview}
                    id={item.portfolio_id}
                  />
                ))}
              </CustomSlider>
            )}
          </div>
          <div className="profile-reviews">
            <p className="profile__title">Отзывы</p>
            {user.user_estimations.map((item) => (
              <FeedbackCard {...item} />
            ))}
          </div>
        </div>
      </Layout>
    );
  }
};

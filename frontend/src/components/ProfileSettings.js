/*import React, { useState } from 'react';
import "./ps.css";
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://46.149.72.161:5000";

const ProfileSettings = ({ profileData, updateProfile }) => {
  const [activeTab, setActiveTab] = useState('personal');
  const [formData, setFormData] = useState({
    personal: {
      username: profileData?.username || '',
      birthDate: profileData?.dob || ''
    },
    contacts: {
      telegram: profileData?.contacts?.telegram || '',
      discord: profileData?.contacts?.discord || '',
      steam: profileData?.contacts?.steam || ''
    },
    password: {
      newPassword: '',
      confirmPassword: ''
    }
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setErrors({});
    setSuccessMessage('');
  };

  const handleChange = (tab, field, value) => {
    setFormData(prev => ({
      ...prev,
      [tab]: {
        ...prev[tab],
        [field]: value
      }
    }));
  };

  const validatePassword = () => {
    const { newPassword, confirmPassword } = formData.password;
    if (newPassword !== confirmPassword) return 'Passwords do not match';
    return '';
  };

  const handleSubmit = async (tab) => {
    setIsLoading(true);
    setErrors({});

    try {
      const token = localStorage.getItem('token');

      if (tab === 'personal') {
        const payload = {
          new_username: 
            formData.personal.username !== profileData.username 
              ? formData.personal.username 
              : null,
          new_dob: 
            formData.personal.birthDate !== profileData.dob 
              ? formData.personal.birthDate 
              : null
        };

        if (payload.new_username === null && payload.new_dob === null) {
          throw new Error("No changes detected");
        }

        const response = await fetch(
          `${API_BASE_URL}/user/credits`,
          {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(payload)
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to update credits');
        }

        const updatedPersonal = {
          username: payload.new_username !== null ? formData.personal.username : profileData.username,
          dob: payload.new_dob !== null ? formData.personal.birthDate : profileData.dob
        };
        await updateProfile({ ...profileData, ...updatedPersonal });
        setSuccessMessage('Personal info updated successfully!');
      } else if (tab === 'contacts') {
        const payload = {
          telegram: 
            formData.contacts.telegram !== profileData.contacts?.telegram 
              ? formData.contacts.telegram 
              : null,
          discord: 
            formData.contacts.discord !== profileData.contacts?.discord 
              ? formData.contacts.discord 
              : null,
          steam: 
            formData.contacts.steam !== profileData.contacts?.steam 
              ? formData.contacts.steam 
              : null
        };

        if (Object.values(payload).every(v => v === null)) {
          throw new Error("No changes detected");
        }

        const response = await fetch(
          `${API_BASE_URL}/user/contacts`,
          {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(payload)
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to update contacts');
        }

        const updatedContacts = {};
        Object.entries(payload).forEach(([key, value]) => {
          if (value !== null) {
            updatedContacts[key] = value;
          }
        });
        
        await updateProfile({ contacts: updatedContacts });
        setSuccessMessage("Contacts updated successfully!");
      } else if (tab === 'password') {
        const passwordError = validatePassword();
        if (passwordError) {
          setErrors({ password: passwordError });
          setIsLoading(false);
          return;
        }

        const newPassword = formData.password.newPassword.trim();
        if (!newPassword) {
          throw new Error("New password is required");
        }

        const payload = {
          new_password: newPassword
        };

        const response = await fetch(
          `${API_BASE_URL}/user/change-password`,
          {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(payload)
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to change password');
        }

        setSuccessMessage('Password changed successfully!');
        setFormData(prev => ({
          ...prev,
          password: { newPassword: '', confirmPassword: '' }
        }));
      }

      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      setErrors({ common: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  // Новая вкладка для подключения Steam
  const handleSteamConnect = () => {
    window.location.href = `${API_BASE_URL}/auth/steam/login`;
  };

  return (
    <div className="settings-container">
      <div className="settings-tabs">
        <div 
          className={`tab ${activeTab === 'personal' ? 'active' : ''}`}
          onClick={() => handleTabChange('personal')}
        >
          Personal Information
        </div>
        <div 
          className={`tab ${activeTab === 'contacts' ? 'active' : ''}`}
          onClick={() => handleTabChange('contacts')}
        >
          Contacts
        </div>
        <div 
          className={`tab ${activeTab === 'password' ? 'active' : ''}`}
          onClick={() => handleTabChange('password')}
        >
          Change Password
        </div>
        <div 
          className={`tab ${activeTab === 'steam' ? 'active' : ''}`}
          onClick={() => handleTabChange('steam')}
        >
          Steam Integration
        </div>
      </div>

      <div className="settings-content">
        {activeTab === 'personal' && (
          <div className="personal-tab">
            <div className="input-group">
              <label>Username</label>
              <input 
                type="text"
                value={formData.personal.username}
                onChange={e => handleChange('personal', 'username', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Date of Birth</label>
              <input 
                type="date"
                value={formData.personal.birthDate ? formData.personal.birthDate.split('T')[0] : ''}
                onChange={e => handleChange('personal', 'birthDate', e.target.value)}
              />
            </div>
            <button 
              className="save-btn"
              onClick={() => handleSubmit('personal')}
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        )}

        {activeTab === 'contacts' && (
          <div className="contacts-tab">
            <div className="input-group">
              <label>Telegram</label>
              <input 
                type="text"
                value={formData.contacts.telegram}
                onChange={e => handleChange('contacts', 'telegram', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Discord</label>
              <input 
                type="text"
                value={formData.contacts.discord}
                onChange={e => handleChange('contacts', 'discord', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Steam</label>
              <input 
                type="text"
                value={formData.contacts.steam}
                onChange={e => handleChange('contacts', 'steam', e.target.value)}
              />
            </div>
            <button 
              className="save-btn"
              onClick={() => handleSubmit('contacts')}
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        )}

        {activeTab === 'password' && (
          <div className="password-tab">
            <div className="input-group">
              <label>New Password</label>
              <input 
                type="password"
                value={formData.password.newPassword}
                onChange={e => handleChange('password', 'newPassword', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Confirm Password</label>
              <input 
                type="password"
                value={formData.password.confirmPassword}
                onChange={e => handleChange('password', 'confirmPassword', e.target.value)}
              />
            </div>
            {errors.password && <p className="error-message">{errors.password}</p>}
            <button 
              className="save-btn"
              onClick={() => handleSubmit('password')}
              disabled={
                isLoading || 
                !formData.password.newPassword || 
                !formData.password.confirmPassword || 
                validatePassword() !== ''
              }
            >
              {isLoading ? 'Updating...' : 'Change Password'}
            </button>
          </div>
        )}

        {activeTab === 'steam' && (
          <div className="steam-tab">
            <p>
              To import your Steam information, connect your Steam account:
            </p>
            <button 
              className="save-btn"
              onClick={handleSteamConnect}
              disabled={isLoading}
            >
              Connect Steam
            </button>
          </div>
        )}
      </div>

      {successMessage && <div className="success-message">{successMessage}</div>}
      {errors.common && <div className="error-message">{errors.common}</div>}
    </div>
  );
};

export default ProfileSettings;*/

import React, { useState } from 'react';
import './ps.css';
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://46.149.72.161:5000";

const ProfileSettings = ({ profileData, updateProfile }) => {
  const [activeTab, setActiveTab] = useState('personal');
  const [formData, setFormData] = useState({
    personal: {
      username: profileData?.username || '',
      birthDate: profileData?.dob || '',
      bio: profileData?.description || ''
    },
    contacts: {
      telegram: profileData?.contacts?.telegram || '',
      discord: profileData?.contacts?.discord || '',
      steam: profileData?.contacts?.steam || ''
    },
    password: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  });

  const [avatarFile, setAvatarFile] = useState(null); // Для аватара
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [isLoadingCredits, setIsLoadingCredits] = useState(false);
  const [isLoadingAvatar, setIsLoadingAvatar] = useState(false);

  // Смена вкладки
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setErrors({});
    setSuccessMessage('');
  };

  // Обновление данных форм
  const handleChange = (tab, field, value) => {
    setFormData(prev => ({
      ...prev,
      [tab]: {
        ...prev[tab],
        [field]: value
      }
    }));
  };

  // 1. Обработчик для основных данных (username, birthDate, bio)
  const handleSavePersonal = async () => {
    setIsLoadingCredits(true);
    setErrors({});

    try {
      const token = localStorage.getItem('token');
      const payload = {
        new_username: 
          formData.personal.username !== profileData.username 
            ? formData.personal.username 
            : null,
        new_dob: 
          formData.personal.birthDate !== profileData.dob 
            ? formData.personal.birthDate 
            : null,
        new_bio: 
          formData.personal.bio !== profileData.description 
            ? formData.personal.bio 
            : null
      };

      // Проверка на отсутствие изменений
      if (Object.values(payload).every(v => v === null)) {
        throw new Error("No changes detected");
      }

      const response = await fetch(
        `${API_BASE_URL}/user/credits`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update personal info');
      }

      const updatedData = {
        username: payload.new_username || profileData.username,
        dob: payload.new_dob || profileData.dob,
        bio: payload.new_bio || profileData.description
      };

      await updateProfile({ ...profileData, ...updatedData });
      setSuccessMessage('Personal info updated successfully!');
    } catch (error) {
      setErrors({ common: error.message });
    } finally {
      setIsLoadingCredits(false);
    }
  };

  // 2. Обработчик для аватара
  const handleUpdateAvatar = async () => {
    setIsLoadingAvatar(true);
    setErrors({});

    if (!avatarFile) {
      throw new Error("Avatar file is required");
    }

    try {
      const token = localStorage.getItem('token');
      const formDataAvatar = new FormData();
      formDataAvatar.append('new_avatar', avatarFile);

      const response = await fetch(
        `${API_BASE_URL}/user/avatar`,
        {
          method: 'PATCH',
          headers: { Authorization: `Bearer ${token}` },
          body: formDataAvatar
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Avatar update failed');
      }

      const data = await response.json();
      await updateProfile({ avatar: data.avatar_url });
      setSuccessMessage('Avatar updated successfully!');
      setAvatarFile(null); // Очистить выбранный файл
    } catch (error) {
      setErrors({ common: error.message });
    } finally {
      setIsLoadingAvatar(false);
    }
  };

  // 3. Обработчик для контактов
  const handleSaveContacts = async () => {
    setIsLoadingCredits(true);
    setErrors({});

    try {
      const token = localStorage.getItem('token');
      const payload = {
        telegram: 
          formData.contacts.telegram !== profileData.contacts?.telegram 
            ? formData.contacts.telegram 
            : null,
        discord: 
          formData.contacts.discord !== profileData.contacts?.discord 
            ? formData.contacts.discord 
            : null,
        steam: 
          formData.contacts.steam !== profileData.contacts?.steam 
            ? formData.contacts.steam 
            : null
      };

      if (Object.values(payload).every(v => v === null)) {
        throw new Error("No changes detected");
      }

      const response = await fetch(
        `${API_BASE_URL}/user/contacts`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update contacts');
      }

      const updatedContacts = {};
      Object.entries(payload).forEach(([key, value]) => {
        if (value !== null) {
          updatedContacts[key] = value;
        }
      });

      await updateProfile({ contacts: updatedContacts });
      setSuccessMessage('Contacts updated successfully!');
    } catch (error) {
      setErrors({ common: error.message });
    } finally {
      setIsLoadingCredits(false);
    }
  };

  // 4. Обработчик для пароля
  const handlePasswordSubmit = async () => {
    setIsLoadingCredits(true);
    setErrors({});

    const { newPassword, confirmPassword } = formData.password;
    if (newPassword !== confirmPassword) {
      setErrors({ password: 'Passwords do not match' });
      setIsLoadingCredits(false);
      return;
    }

    if (!newPassword) {
      throw new Error("New password is required");
    }

    try {
      const token = localStorage.getItem('token');
      const payload = {
        current_password: formData.password.currentPassword,
        new_password: newPassword
      };

      const response = await fetch(
        `${API_BASE_URL}/user/change-password`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Password change failed');
      }

      setSuccessMessage('Password changed successfully!');
      setFormData(prev => ({
        ...prev,
        password: { currentPassword: '', newPassword: '', confirmPassword: '' }
      }));
    } catch (error) {
      setErrors({ common: error.message });
    } finally {
      setIsLoadingCredits(false);
    }
  };

  return (
    <div className="settings-container">
      <div className="settings-tabs">
        <div 
          className={`tab ${activeTab === 'personal' ? 'active' : ''}`}
          onClick={() => handleTabChange('personal')}
        >
          Personal Information
        </div>
        <div 
          className={`tab ${activeTab === 'contacts' ? 'active' : ''}`}
          onClick={() => handleTabChange('contacts')}
        >
          Contacts
        </div>
        <div 
          className={`tab ${activeTab === 'password' ? 'active' : ''}`}
          onClick={() => handleTabChange('password')}
        >
          Change Password
        </div>
        <div 
          className={`tab ${activeTab === 'steam' ? 'active' : ''}`}
          onClick={() => handleTabChange('steam')}
        >
          Steam Integration
        </div>
      </div>

      <div className="settings-content">
        {/* Вкладка Personal Information */}
        {activeTab === 'personal' && (
          <div className="personal-tab">
            {/* Блок 1: Основные данные */}
            <div className="personal-group">
              <div className="input-group">
                <label>Username</label>
                <input 
                  type="text"
                  value={formData.personal.username}
                  onChange={e => handleChange('personal', 'username', e.target.value)}
                />
              </div>
              <div className="input-group">
                <label>Date of Birth</label>
                <input 
                  type="date"
                  value={formData.personal.birthDate}
                  onChange={e => handleChange('personal', 'birthDate', e.target.value)}
                />
              </div>
              <div className="input-group">
                <label>Bio</label>
                <textarea 
                  className="bio-input"
                  value={formData.personal.bio}
                  onChange={e => handleChange('personal', 'bio', e.target.value)}
                />
              </div>
              <button 
                className="save-btn"
                onClick={handleSavePersonal}
                disabled={isLoadingCredits}
              >
                {isLoadingCredits ? 'Saving...' : 'Save Changes'}
              </button>
            </div>

            {/* Блок 2: Обновление аватара */}
            <div className="avatar-group" style={{ marginTop: '40px' }}>
              <div className="input-group">
                <label>Avatar</label>
                <input 
                  type="file" 
                  accept="image/*"
                  onChange={(e) => setAvatarFile(e.target.files[0])}
                />
                {avatarFile && (
                  <img 
                    src={URL.createObjectURL(avatarFile)} 
                    alt="Preview" 
                    className="avatar-preview"
                  />
                )}
              </div>
              <button 
                className="save-btn"
                onClick={handleUpdateAvatar}
                disabled={!avatarFile || isLoadingAvatar}
              >
                {isLoadingAvatar ? 'Updating...' : 'Update Avatar'}
              </button>
            </div>
          </div>
        )}

        {/* Вкладка Contacts */}
        {activeTab === 'contacts' && (
          <div className="contacts-tab">
            <div className="input-group">
              <label>Telegram</label>
              <input 
                type="text"
                value={formData.contacts.telegram}
                onChange={e => handleChange('contacts', 'telegram', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Discord</label>
              <input 
                type="text"
                value={formData.contacts.discord}
                onChange={e => handleChange('contacts', 'discord', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Steam</label>
              <input 
                type="text"
                value={formData.contacts.steam}
                onChange={e => handleChange('contacts', 'steam', e.target.value)}
              />
            </div>
            <button 
              className="save-btn"
              onClick={handleSaveContacts}
              disabled={isLoadingCredits}
            >
              {isLoadingCredits ? 'Saving...' : 'Save Contacts'}
            </button>
          </div>
        )}

        {/* Вкладка Password */}
        {activeTab === 'password' && (
          <div className="password-tab">
            <div className="input-group">
              <label>Current Password</label>
              <input 
                type="password"
                value={formData.password.currentPassword}
                onChange={e => handleChange('password', 'currentPassword', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>New Password</label>
              <input 
                type="password"
                value={formData.password.newPassword}
                onChange={e => handleChange('password', 'newPassword', e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Confirm Password</label>
              <input 
                type="password"
                value={formData.password.confirmPassword}
                onChange={e => handleChange('password', 'confirmPassword', e.target.value)}
              />
            </div>
            {errors.password && <p className="error">{errors.password}</p>}
            <button 
              className="save-btn"
              onClick={handlePasswordSubmit}
              disabled={
                isLoadingCredits || 
                !formData.password.newPassword || 
                formData.password.newPassword !== formData.password.confirmPassword
              }
            >
              {isLoadingCredits ? 'Updating...' : 'Change Password'}
            </button>
          </div>
        )}

        {/* Вкладка Steam Integration */}
        {activeTab === 'steam' && (
          <div className="steam-tab">
            <p>To connect Steam, click the button below:</p>
            <button 
              className="save-btn"
              onClick={() => window.location.href = `${API_BASE_URL}/auth/steam/login`}
            >
              Connect Steam
            </button>
          </div>
        )}
      </div>

      {/* Сообщения об успехе/ошибках */}
      {successMessage && <div className="success">{successMessage}</div>}
      {errors.common && <div className="error">{errors.common}</div>}
    </div>
  );
};

export default ProfileSettings;
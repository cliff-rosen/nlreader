import { Layout, Space, Typography, Menu, MenuProps } from 'antd';

const contentStyle = {
  padding: '0',
  backgroundColor: '#fff',
  xborder: 'dashed'
};

const navigationData = [
  { key: 'batch', label: 'Select Batch' },
  { key: 'clean', label: 'Clean' },
  { key: 'articles', label: 'Extract Articles' },
  { key: 'topics', label: 'Compile Topics' },
  { key: 'read', label: 'Read' },
];

function LeftNav({ currentScreen, onScreenChange }) {

  const onClick = (e) => {
    onScreenChange(e.key);
  };

  return (
    <Layout.Sider width={250} style={contentStyle}>
      <Menu
        style={{
          width: 256,
        }}
        mode="inline"
        items={navigationData}
        onClick={onClick}
      />
    </Layout.Sider>
  );
}

export default LeftNav;

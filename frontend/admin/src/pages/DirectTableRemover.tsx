// eslint-disable  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82UzJKMWRRPT06YTQ5NzM3NDQ=

import React from 'react';
import { Button, message } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';

interface DirectTableRemoverProps {
  onRemoveFirstTable: () => void;
}
// eslint-disable  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82UzJKMWRRPT06YTQ5NzM3NDQ=

// 直接删除第一个表的组件
const DirectTableRemover: React.FC<DirectTableRemoverProps> = ({ onRemoveFirstTable }) => {
  const handleClick = () => {
    onRemoveFirstTable();
  };

  return (
    <Button
      type="primary"
      danger
      icon={<DeleteOutlined />}
      onClick={handleClick}
      style={{ marginLeft: '8px' }}
    >
      删除第一个表
    </Button>
  );
};

export default DirectTableRemover;
